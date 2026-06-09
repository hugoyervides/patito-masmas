'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import dynamic from 'next/dynamic';
import { DEFAULT_CODE, registerPatitoLanguage } from '@/lib/patito-language';

const Editor = dynamic(() => import('@monaco-editor/react'), { ssr: false });

// Same-origin in production; point to the FastAPI dev server during `next dev`
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || '';

export default function Home() {
  const [examples, setExamples] = useState([]);
  const [stdinValue, setStdinValue] = useState('');
  const [output, setOutput] = useState('Presiona Ejecutar para correr tu programa.');
  const [compilerOutput, setCompilerOutput] = useState('');
  const [status, setStatus] = useState('');
  const [isError, setIsError] = useState(false);
  const [running, setRunning] = useState(false);
  const editorRef = useRef(null);
  const runRef = useRef(() => {});

  useEffect(() => {
    fetch(`${API_BASE}/api/examples`)
      .then((res) => res.json())
      .then((data) => setExamples(data.examples || []))
      .catch(() => setExamples([]));
  }, []);

  const runProgram = useCallback(async () => {
    if (!editorRef.current) return;
    setRunning(true);
    setStatus('Ejecutando...');
    setOutput('');
    setIsError(false);

    try {
      const res = await fetch(`${API_BASE}/api/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code: editorRef.current.getValue(),
          stdin: stdinValue,
        }),
      });

      if (!res.ok) {
        const detail = (await res.json().catch(() => ({}))).detail || res.statusText;
        setOutput(`Error: ${detail}`);
        setIsError(true);
        setStatus('');
        return;
      }

      const result = await res.json();
      setCompilerOutput(
        (result.compiler_output || '') + (result.compiler_errors ? `\n${result.compiler_errors}` : ''),
      );

      if (result.phase === 'compile') {
        setOutput(
          result.timed_out
            ? 'El compilador excedio el tiempo limite.'
            : `Error de compilacion:\n\n${result.compiler_output || ''}${result.compiler_errors || ''}`,
        );
        setIsError(true);
        setStatus(`Fallo la compilacion (${result.duration_ms} ms)`);
        return;
      }

      let text = result.stdout || '';
      if (result.timed_out) {
        text += '\n[El programa excedio el tiempo limite y fue terminado]';
      }
      if (result.stderr) {
        text += `\n--- stderr ---\n${result.stderr}`;
      }
      setOutput(text.trim() || '(sin salida)');
      setIsError(!result.ok);
      setStatus(`${result.ok ? 'Ejecucion exitosa' : 'Termino con errores'} (${result.duration_ms} ms)`);
    } catch (err) {
      setOutput(`Error de red: ${err.message}`);
      setIsError(true);
      setStatus('');
    } finally {
      setRunning(false);
    }
  }, [stdinValue]);

  // Keep the Monaco keybinding pointing at the latest run closure
  useEffect(() => {
    runRef.current = runProgram;
  }, [runProgram]);

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
          <button onClick={runProgram} disabled={running} title="Ctrl/Cmd + Enter">
            ▶ Ejecutar
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
          <section className="panel">
            <h2>Entrada (stdin)</h2>
            <textarea
              value={stdinValue}
              onChange={(event) => setStdinValue(event.target.value)}
              placeholder="Una linea por cada 'lee(...)' del programa"
            />
          </section>
          <section className="panel grow">
            <h2>Salida</h2>
            <pre className={`output${isError ? ' error' : ''}`}>{output}</pre>
          </section>
          <details className="panel">
            <summary>Salida del compilador</summary>
            <pre className="output small">{compilerOutput}</pre>
          </details>
        </div>
      </main>

      <footer>
        <span>{status}</span>
        <span className="hint">Ctrl/Cmd + Enter para ejecutar</span>
      </footer>
    </div>
  );
}
