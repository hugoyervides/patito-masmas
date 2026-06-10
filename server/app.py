#Patito ++ Web IDE backend
#Serves the Monaco editor frontend and compiles/runs Patito ++ code in
#resource-limited subprocesses so untrusted code can't take down the host.
import asyncio
import json
import os
import resource
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

ROOT_DIR = Path(__file__).resolve().parent.parent
COMPILER = ROOT_DIR / "compile.py"
VM = ROOT_DIR / "patito_vm.py"
EXAMPLES_DIR = ROOT_DIR / "code_examples"
#Static export produced by `npm run build` in frontend/
FRONTEND_DIST = Path(os.environ.get("PATITO_FRONTEND_DIST", str(ROOT_DIR / "frontend" / "out")))

#Hard limits for untrusted code (overridable through environment variables)
MAX_CODE_BYTES = int(os.environ.get("PATITO_MAX_CODE_BYTES", 64 * 1024))
MAX_STDIN_BYTES = int(os.environ.get("PATITO_MAX_STDIN_BYTES", 16 * 1024))
MAX_OUTPUT_BYTES = int(os.environ.get("PATITO_MAX_OUTPUT_BYTES", 64 * 1024))
COMPILE_TIMEOUT_S = int(os.environ.get("PATITO_COMPILE_TIMEOUT", 15))
RUN_TIMEOUT_S = int(os.environ.get("PATITO_RUN_TIMEOUT", 10))
#Interactive sessions may legitimately sit waiting for user input, so they
#get a generous wall-clock limit; RLIMIT_CPU still kills busy loops fast
SESSION_TIMEOUT_S = int(os.environ.get("PATITO_SESSION_TIMEOUT", 300))
CPU_SECONDS = int(os.environ.get("PATITO_CPU_SECONDS", 5))
MEMORY_BYTES = int(os.environ.get("PATITO_MEMORY_BYTES", 1024 * 1024 * 1024))
MAX_FILE_BYTES = int(os.environ.get("PATITO_MAX_FILE_BYTES", 8 * 1024 * 1024))
MAX_CONCURRENT = int(os.environ.get("PATITO_MAX_CONCURRENT", 2))
RATE_LIMIT_RUNS = int(os.environ.get("PATITO_RATE_LIMIT_RUNS", 30))
RATE_LIMIT_WINDOW_S = int(os.environ.get("PATITO_RATE_LIMIT_WINDOW", 60))
#Only trust X-Forwarded-For when explicitly behind a reverse proxy
TRUST_PROXY = os.environ.get("PATITO_TRUST_PROXY", "") == "1"

app = FastAPI(title="Patito ++ Web IDE", docs_url=None, redoc_url=None)

#For local development only: allow the Next.js dev server origin, e.g.
#PATITO_CORS_ORIGINS=http://localhost:3000 (production serves both from one origin)
_cors_origins = [o for o in os.environ.get("PATITO_CORS_ORIGINS", "").split(",") if o]
if _cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

_run_slots = threading.BoundedSemaphore(MAX_CONCURRENT)
_rate_lock = threading.Lock()
_rate_hits = {}


class RunRequest(BaseModel):
    code: str
    stdin: str = ""


def _client_ip(request: Request) -> str:
    if TRUST_PROXY:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _rate_limited(ip: str) -> bool:
    now = time.monotonic()
    with _rate_lock:
        hits = [t for t in _rate_hits.get(ip, []) if now - t < RATE_LIMIT_WINDOW_S]
        if len(hits) >= RATE_LIMIT_RUNS:
            _rate_hits[ip] = hits
            return True
        hits.append(now)
        _rate_hits[ip] = hits
        #Drop stale entries so the table can't grow unbounded
        if len(_rate_hits) > 10000:
            for key in [k for k, v in _rate_hits.items() if not v or now - v[-1] > RATE_LIMIT_WINDOW_S]:
                del _rate_hits[key]
    return False


def _apply_rlimits():
    #Runs in the child right before exec: cap CPU time, address space,
    #file size and open files so a hostile program can't exhaust the host
    resource.setrlimit(resource.RLIMIT_CPU, (CPU_SECONDS, CPU_SECONDS + 1))
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_BYTES, MEMORY_BYTES))
    resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_FILE_BYTES, MAX_FILE_BYTES))
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def _truncate(data: bytes) -> str:
    text = data[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace")
    if len(data) > MAX_OUTPUT_BYTES:
        text += "\n... [output truncated]"
    return text


def _run_sandboxed(cmd, cwd, stdin_data: bytes, timeout: int):
    env = {
        "PATH": os.defpath,
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONIOENCODING": "utf-8",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
    }
    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        preexec_fn=_apply_rlimits,
        start_new_session=True,
    )
    timed_out = False
    try:
        stdout, stderr = proc.communicate(stdin_data, timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        stdout, stderr = proc.communicate()
    return _truncate(stdout), _truncate(stderr), proc.returncode, timed_out


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/api/examples")
def list_examples():
    examples = []
    for path in sorted(EXAMPLES_DIR.glob("*.dpp")):
        examples.append({"name": path.stem, "content": path.read_text(encoding="utf-8")})
    return {"examples": examples}


@app.post("/api/compile")
def compile_only(payload: RunRequest, request: Request):
    #Compile without running: returns the quadruples and constant table so
    #students can study the intermediate representation the compiler emits
    if len(payload.code.encode("utf-8")) > MAX_CODE_BYTES:
        raise HTTPException(status_code=413, detail="Code too large")
    if _rate_limited(_client_ip(request)):
        raise HTTPException(status_code=429, detail="Too many runs, slow down")
    if not _run_slots.acquire(blocking=False):
        raise HTTPException(status_code=429, detail="Server busy, try again in a moment")
    started = time.monotonic()
    workdir = tempfile.mkdtemp(prefix="patito_")
    try:
        ok, stdout, stderr, timed_out = _compile_in_workdir(payload.code, workdir)
        quadruples, constants = _read_artifacts(workdir)
        return {
            "ok": ok,
            "compiler_output": stdout,
            "compiler_errors": stderr,
            "timed_out": timed_out,
            "quadruples": quadruples,
            "constants": constants,
            "duration_ms": int((time.monotonic() - started) * 1000),
        }
    finally:
        _run_slots.release()
        shutil.rmtree(workdir, ignore_errors=True)


@app.post("/api/run")
def run_code(payload: RunRequest, request: Request):
    if len(payload.code.encode("utf-8")) > MAX_CODE_BYTES:
        raise HTTPException(status_code=413, detail="Code too large")
    if len(payload.stdin.encode("utf-8")) > MAX_STDIN_BYTES:
        raise HTTPException(status_code=413, detail="Stdin too large")
    if _rate_limited(_client_ip(request)):
        raise HTTPException(status_code=429, detail="Too many runs, slow down")
    if not _run_slots.acquire(blocking=False):
        raise HTTPException(status_code=429, detail="Server busy, try again in a moment")
    try:
        return _compile_and_run(payload)
    finally:
        _run_slots.release()


def _compile_and_run(payload: RunRequest):
    started = time.monotonic()
    workdir = tempfile.mkdtemp(prefix="patito_")
    try:
        compile_ok, compiler_stdout, compiler_stderr, compile_timed_out = _compile_in_workdir(
            payload.code, workdir
        )
        quadruples, constants = _read_artifacts(workdir)
        if not compile_ok:
            return {
                "ok": False,
                "phase": "compile",
                "stdout": "",
                "stderr": "",
                "compiler_output": compiler_stdout,
                "compiler_errors": compiler_stderr,
                "quadruples": quadruples,
                "constants": constants,
                "timed_out": compile_timed_out,
                "duration_ms": int((time.monotonic() - started) * 1000),
            }

        stdout, stderr, returncode, run_timed_out = _run_sandboxed(
            [sys.executable, str(VM), "quads.out"],
            cwd=workdir,
            stdin_data=payload.stdin.encode("utf-8"),
            timeout=RUN_TIMEOUT_S,
        )
        #RLIMIT_CPU kills with SIGXCPU before the wall-clock timeout fires;
        #report it as a timeout so the user gets a clear message
        if returncode == -signal.SIGXCPU:
            run_timed_out = True
        return {
            "ok": returncode == 0 and not run_timed_out,
            "phase": "run",
            "stdout": stdout,
            "stderr": stderr,
            "compiler_output": compiler_stdout,
            "compiler_errors": compiler_stderr,
            "quadruples": quadruples,
            "constants": constants,
            "timed_out": run_timed_out,
            "duration_ms": int((time.monotonic() - started) * 1000),
        }
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def _kill_group(pid: int):
    try:
        os.killpg(pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass


def _compile_in_workdir(code: str, workdir: str):
    #Shared by the REST endpoint and the interactive WebSocket session
    source = Path(workdir) / "program.dpp"
    source.write_text(code, encoding="utf-8")
    stdout, stderr, _, timed_out = _run_sandboxed(
        [sys.executable, str(COMPILER), str(source), "quads.out"],
        cwd=workdir,
        stdin_data=b"",
        timeout=COMPILE_TIMEOUT_S,
    )
    #The compiler exits with status 0 even on syntax errors, so success
    #is determined by whether the quadruple file was produced
    ok = not timed_out and (Path(workdir) / "quads.out").exists()
    return ok, stdout, stderr, timed_out


def _read_artifacts(workdir):
    #Parse the generated quadruples and constant table so the UI can show
    #the intermediate representation for teaching/debugging
    quadruples = []
    constants = []
    quads_file = Path(workdir) / "quads.out"
    consts_file = Path(workdir) / "c_quads.out"
    if quads_file.exists():
        for line in quads_file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                quadruples.append(json.loads(line))
    if consts_file.exists():
        for line in consts_file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                constants.append(json.loads(line))
    return quadruples, constants


@app.websocket("/api/session")
async def interactive_session(ws: WebSocket):
    #Interactive run: the browser terminal sends {"type": "run", "code": ...}
    #then {"type": "stdin", "data": ...} lines; the server streams stdout and
    #stderr back as they are produced so 'lee'/'escribe' work like a console
    await ws.accept()
    try:
        msg = await asyncio.wait_for(ws.receive_json(), timeout=30)
    except (asyncio.TimeoutError, WebSocketDisconnect, ValueError):
        await ws.close()
        return

    code = msg.get("code", "") if msg.get("type") == "run" else None
    debug_mode = bool(msg.get("debug"))
    if code is None:
        await ws.send_json({"type": "error", "message": "Se esperaba un mensaje 'run'"})
        await ws.close()
        return
    if len(code.encode("utf-8")) > MAX_CODE_BYTES:
        await ws.send_json({"type": "error", "message": "El codigo es demasiado grande"})
        await ws.close()
        return
    if _rate_limited(_client_ip(ws)):
        await ws.send_json({"type": "error", "message": "Demasiadas ejecuciones, espera un momento"})
        await ws.close()
        return
    if not _run_slots.acquire(blocking=False):
        await ws.send_json({"type": "error", "message": "Servidor ocupado, intenta en un momento"})
        await ws.close()
        return

    started = time.monotonic()
    workdir = tempfile.mkdtemp(prefix="patito_")
    proc = None
    try:
        loop = asyncio.get_running_loop()
        compile_ok, compiler_stdout, compiler_stderr, compile_timed_out = await loop.run_in_executor(
            None, _compile_in_workdir, code, workdir
        )
        await ws.send_json({"type": "compiler", "data": compiler_stdout + compiler_stderr})
        if compile_ok:
            quadruples, constants = await loop.run_in_executor(None, _read_artifacts, workdir)
            await ws.send_json({"type": "quadruples", "quadruples": quadruples, "constants": constants})
        if not compile_ok:
            await ws.send_json({
                "type": "compile_error",
                "data": compiler_stdout + compiler_stderr,
                "timed_out": compile_timed_out,
                "duration_ms": int((time.monotonic() - started) * 1000),
            })
            await ws.close()
            return

        env = {
            "PATH": os.defpath,
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONIOENCODING": "utf-8",
            #Unbuffered so 'escribe' prompts reach the terminal before 'lee' blocks
            "PYTHONUNBUFFERED": "1",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
        }
        #In debug mode the VM gets two extra pipes: one to emit JSON trace
        #events (current quadruple, memory snapshots) and one to receive
        #step/continue/pause commands, keeping stdin/stdout for the program
        vm_cmd = [sys.executable, "-u", str(VM), "quads.out"]
        pass_fds = ()
        event_read_fd = command_write_fd = None
        if debug_mode:
            event_read_fd, event_write_fd = os.pipe()
            command_read_fd, command_write_fd = os.pipe()
            vm_cmd += ["--debug", str(event_write_fd), str(command_read_fd)]
            pass_fds = (event_write_fd, command_read_fd)

        proc = await asyncio.create_subprocess_exec(
            *vm_cmd,
            cwd=workdir,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
            preexec_fn=_apply_rlimits,
            start_new_session=True,
            pass_fds=pass_fds,
        )

        command_pipe = None
        event_reader = None
        event_transport = None
        if debug_mode:
            #Close the child's ends in this process and wrap ours
            os.close(event_write_fd)
            os.close(command_read_fd)
            command_pipe = os.fdopen(command_write_fd, "w", buffering=1)
            command_write_fd = None
            event_reader = asyncio.StreamReader()
            event_transport, _ = await loop.connect_read_pipe(
                lambda: asyncio.StreamReaderProtocol(event_reader),
                os.fdopen(event_read_fd, "rb"),
            )
            event_read_fd = None

        output_bytes = 0

        async def pump(stream, kind):
            nonlocal output_bytes
            while True:
                chunk = await stream.read(4096)
                if not chunk:
                    return
                output_bytes += len(chunk)
                try:
                    await ws.send_json({"type": kind, "data": chunk.decode("utf-8", "replace")})
                except Exception:
                    return
                if output_bytes > MAX_OUTPUT_BYTES:
                    try:
                        await ws.send_json({"type": "stderr", "data": "\n[Salida truncada: se excedio el limite]\n"})
                    except Exception:
                        pass
                    _kill_group(proc.pid)
                    return

        async def pump_debug_events():
            while True:
                line = await event_reader.readline()
                if not line:
                    return
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                try:
                    await ws.send_json({"type": "debug", **event})
                except Exception:
                    return

        async def feed_stdin():
            #Returns when the client disconnects or asks to kill the run
            stdin_bytes = 0
            while True:
                message = await ws.receive_json()
                msg_type = message.get("type")
                if msg_type == "stdin":
                    data = str(message.get("data", "")).encode("utf-8")
                    stdin_bytes += len(data)
                    if stdin_bytes > MAX_STDIN_BYTES:
                        return
                    try:
                        proc.stdin.write(data)
                        await proc.stdin.drain()
                    except (ConnectionResetError, BrokenPipeError):
                        return
                elif msg_type in ("step", "continue", "pause") and command_pipe is not None:
                    try:
                        command_pipe.write(msg_type + "\n")
                    except (BrokenPipeError, ValueError):
                        pass
                elif msg_type == "kill":
                    return

        pump_out = asyncio.create_task(pump(proc.stdout, "stdout"))
        pump_err = asyncio.create_task(pump(proc.stderr, "stderr"))
        pump_dbg = asyncio.create_task(pump_debug_events()) if debug_mode else None
        wait_task = asyncio.create_task(proc.wait())
        feeder = asyncio.create_task(feed_stdin())

        timed_out = False
        done, _ = await asyncio.wait(
            {wait_task, feeder}, timeout=SESSION_TIMEOUT_S, return_when=asyncio.FIRST_COMPLETED
        )
        if wait_task not in done:
            #Session hit the wall-clock limit, or the client went away/asked
            #to stop: kill the program either way
            timed_out = not done
            _kill_group(proc.pid)
            await wait_task
        feeder.cancel()
        pending = [pump_out, pump_err, feeder]
        if pump_dbg is not None:
            pending.append(pump_dbg)
        await asyncio.gather(*pending, return_exceptions=True)
        if event_transport is not None:
            event_transport.close()
        if command_pipe is not None:
            try:
                command_pipe.close()
            except (BrokenPipeError, OSError):
                pass

        returncode = proc.returncode
        if returncode == -signal.SIGXCPU:
            timed_out = True
        try:
            await ws.send_json({
                "type": "exit",
                "code": returncode,
                "timed_out": timed_out,
                "duration_ms": int((time.monotonic() - started) * 1000),
            })
            await ws.close()
        except Exception:
            pass
    except WebSocketDisconnect:
        pass
    finally:
        if proc is not None and proc.returncode is None:
            _kill_group(proc.pid)
        _run_slots.release()
        shutil.rmtree(workdir, ignore_errors=True)


#Serve the Next.js static export (mounted last so /api routes win)
if FRONTEND_DIST.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
