#Patito ++ Web IDE backend
#Serves the Monaco editor frontend and compiles/runs Patito ++ code in
#resource-limited subprocesses so untrusted code can't take down the host.
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

from fastapi import FastAPI, HTTPException, Request
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
        source = Path(workdir) / "program.dpp"
        source.write_text(payload.code, encoding="utf-8")
        quads = Path(workdir) / "quads.out"

        compiler_stdout, compiler_stderr, _, compile_timed_out = _run_sandboxed(
            [sys.executable, str(COMPILER), str(source), "quads.out"],
            cwd=workdir,
            stdin_data=b"",
            timeout=COMPILE_TIMEOUT_S,
        )
        #The compiler exits with status 0 even on syntax errors, so success
        #is determined by whether the quadruple file was produced
        if compile_timed_out or not quads.exists():
            return {
                "ok": False,
                "phase": "compile",
                "stdout": "",
                "stderr": "",
                "compiler_output": compiler_stdout,
                "compiler_errors": compiler_stderr,
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
            "timed_out": run_timed_out,
            "duration_ms": int((time.monotonic() - started) * 1000),
        }
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


#Serve the Next.js static export (mounted last so /api routes win)
if FRONTEND_DIST.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
