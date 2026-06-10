'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import dynamic from 'next/dynamic';
import { DEFAULT_CODE, registerPatitoLanguage } from '@/lib/patito-language';
import TerminalPane from '@/components/TerminalPane';
import QuadruplesView from '@/components/QuadruplesView';

const Editor = dynamic(() => import('@monaco-editor/react'), { ssr: false });

// Same-origin in production; point to the FastAPI dev server during `next dev`
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || '';

const DIM = '\x1b[90m';
const RED = '\x1b[31m';
const RESET = '\x1b[0m';

function wsUrl() {
  const base = API_BASE || window.location.origin;
  return `${base.replace(/^http/, 'ws')}/api/session`;
}

export default function Home() {
  const [examples, setExamples] = useState([]);
  const [compilerOutput, setCompilerOutput] = useState('');
  const [status, setStatus] = useState('');
  const [running, setRunning] = useState(false);
  const [compiling, setCompiling] = useState(false);
  const [quadruples, setQuadruples] = useState([]);
  const [constants, setConstants] = useState([]);
  const [activeTab, setActiveTab] = useState('terminal');

  const editorRef = useRef(null);
  const termRef = useRef(null);
  const wsRef = useRef(null);
  const runningRef = useRef(false);
  const lineBufferRef = useRef('');

  useEffect(() => {
    fetch(`${API_BASE}/api/examples`)
      .then((res) => res.json())
      .then((data) => setExamples(data.examples || []))
      .catch(() => setExamples([]));
  }, []);

  const setRunningState = useCallback((value) => {
    runningRef.current = value;
    setRunning(value);
  }, []);

  const stopProgram = useCallback(() => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'kill' }));
    }
    wsRef.current?.close();
  }, []);

  const runProgram = useCallback(() => {
    if (runningRef.current) {
      stopProgram();
      return;
    }
    const term = termRef.current;
    if (!editorRef.current || !term) return;

    term.reset();
    term.writeln(`${DIM}── Ejecutando ──${RESET}`);
    term.focus();
    lineBufferRef.current = '';
    setStatus('Ejecutando...');
    setCompilerOutput('');
    setActiveTab('terminal');
    setRunningState(true);

    const ws = new WebSocket(wsUrl());
    wsRef.current = ws;

    ws.onopen = () => {
      ws.send(JSON.stringify({ type: 'run', code: editorRef.current.getValue() }));
    };

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      switch (msg.type) {
        case 'stdout':
          term.write(msg.data);
          break;
        case 'stderr':
          term.write(`${RED}${msg.data}${RESET}`);
          break;
        case 'compiler':
          setCompilerOutput(msg.data);
          break;
        case 'quadruples':
          setQuadruples(msg.quadruples || []);
          setConstants(msg.constants || []);
          break;
        case 'compile_error':
          term.write(`${RED}Error de compilacion:\n\n${msg.data}${RESET}`);
          setStatus(`Fallo la compilacion (${msg.duration_ms} ms)`);
          break;
        case 'exit': {
          const note = msg.timed_out
            ? '[El programa excedio el tiempo limite y fue terminado]'
            : `[Proceso terminado con codigo ${msg.code}]`;
          term.write(`\n${DIM}${note}${RESET}\n`);
          setStatus(
            `${msg.code === 0 && !msg.timed_out ? 'Ejecucion exitosa' : 'Termino con errores'} (${msg.duration_ms} ms)`,
          );
          break;
        }
        case 'error':
          term.write(`${RED}${msg.message}${RESET}\n`);
          setStatus('');
          break;
        default:
          break;
      }
    };

    ws.onerror = () => {
      term.write(`${RED}Error de conexion con el servidor${RESET}\n`);
    };

    ws.onclose = () => {
      if (wsRef.current === ws) wsRef.current = null;
      setRunningState(false);
    };
  }, [setRunningState, stopProgram]);

  const compileOnly = useCallback(async () => {
    if (!editorRef.current || runningRef.current) return;
    setCompiling(true);
    setStatus('Compilando...');
    try {
      const res = await fetch(`${API_BASE}/api/compile`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: editorRef.current.getValue() }),
      });
      if (!res.ok) {
        const detail = (await res.json().catch(() => ({}))).detail || res.statusText;
        setStatus(`Error: ${detail}`);
        return;
      }
      const result = await res.json();
      setCompilerOutput((result.compiler_output || '') + (result.compiler_errors || ''));
      setQuadruples(result.quadruples || []);
      setConstants(result.constants || []);
      if (result.ok) {
        setActiveTab('quads');
        setStatus(`Compilacion exitosa: ${result.quadruples.length} cuadruplos (${result.duration_ms} ms)`);
      } else {
        const term = termRef.current;
        if (term) {
          term.reset();
          term.write(`${RED}Error de compilacion:\n\n${result.compiler_output || ''}${result.compiler_errors || ''}${RESET}`);
        }
        setActiveTab('terminal');
        setStatus(`Fallo la compilacion (${result.duration_ms} ms)`);
      }
    } catch (err) {
      setStatus(`Error de red: ${err.message}`);
    } finally {
      setCompiling(false);
    }
  }, []);

  // The terminal's onData handler is registered once, so it reaches the
  // current run through refs
  const runRef = useRef(runProgram);
  useEffect(() => {
    runRef.current = runProgram;
  }, [runProgram]);

  const handleTermReady = useCallback((term) => {
    termRef.current = term;
    term.writeln(`${DIM}Terminal de Patito ++ — la salida y la entrada del programa viven aqui.${RESET}`);
    term.writeln(`${DIM}Presiona Ejecutar (o Ctrl/Cmd + Enter en el editor) para empezar.${RESET}`);

    term.onData((data) => {
      if (!runningRef.current) return;
      const ws = wsRef.current;
      for (const char of data) {
        if (char === '\r') {
          term.write('\r\n');
          if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'stdin', data: `${lineBufferRef.current}\n` }));
          }
          lineBufferRef.current = '';
        } else if (char === '\x7f') {
          if (lineBufferRef.current.length > 0) {
            lineBufferRef.current = lineBufferRef.current.slice(0, -1);
            term.write('\b \b');
          }
        } else if (char === '\x03') {
          //Ctrl+C stops the running program
          if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'kill' }));
          }
        } else if (char >= ' ') {
          lineBufferRef.current += char;
          term.write(char);
        }
      }
    });
  }, []);

  const handleEditorMount = useCallback((editor, monaco) => {
    editorRef.current = editor;
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => runRef.current());
  }, []);

  const loadExample = useCallback((event) => {
    const example = examples.find((item) => item.name === event.target.value);
    if (example && editorRef.current) {
      editorRef.current.setValue(example.content);
    }
  }, [examples]);

  return (
    <div className="ide">
      <header>
        <div className="brand">
          <span className="logo">🦆</span>
          <h1>Patito ++ <span className="subtitle">Web IDE</span></h1>
        </div>
        <div className="toolbar">
          <select defaultValue="" onChange={loadExample} title="Cargar ejemplo">
            <option value="" disabled>Ejemplos...</option>
            {examples.map((example) => (
              <option key={example.name} value={example.name}>{example.name}</option>
            ))}
          </select>
          <button
            className="secondary"
            onClick={compileOnly}
            disabled={running || compiling}
            title="Compilar sin ejecutar para inspeccionar los cuadruplos"
          >
            ⚙ Compilar
          </button>
          <button
            className={running ? 'stop' : ''}
            onClick={runProgram}
            disabled={compiling}
            title="Ctrl/Cmd + Enter"
          >
            {running ? '■ Detener' : '▶ Ejecutar'}
          </button>
        </div>
      </header>

      <main>
        <div className="editor-pane">
          <Editor
            defaultLanguage="patito"
            defaultValue={DEFAULT_CODE}
            theme="patito-dark"
            beforeMount={registerPatitoLanguage}
            onMount={handleEditorMount}
            options={{
              fontSize: 14,
              minimap: { enabled: false },
              scrollBeyondLastLine: false,
              tabSize: 4,
              automaticLayout: true,
            }}
          />
        </div>
        <div className="side">
          <div className="tabs">
            <button
              className={`tab${activeTab === 'terminal' ? ' active' : ''}`}
              onClick={() => setActiveTab('terminal')}
            >
              Terminal
            </button>
            <button
              className={`tab${activeTab === 'quads' ? ' active' : ''}`}
              onClick={() => setActiveTab('quads')}
            >
              Cuadruplos{quadruples.length > 0 ? ` (${quadruples.length})` : ''}
            </button>
          </div>
          {/* The terminal stays mounted (xterm keeps its buffer); only hidden via CSS */}
          <section className={`panel grow${activeTab === 'terminal' ? '' : ' hidden'}`}>
            <TerminalPane onReady={handleTermReady} />
          </section>
          <section className={`panel grow scroll${activeTab === 'quads' ? '' : ' hidden'}`}>
            <QuadruplesView quadruples={quadruples} constants={constants} />
          </section>
          <details className="panel">
            <summary>Salida del compilador</summary>
            <pre className="output small">{compilerOutput}</pre>
          </details>
        </div>
      </main>

      <footer>
        <span>{status}</span>
        <span className="hint">Ctrl/Cmd + Enter para ejecutar · Ctrl+C en la terminal para detener</span>
      </footer>
    </div>
  );
}
