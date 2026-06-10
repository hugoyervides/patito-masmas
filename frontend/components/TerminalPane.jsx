'use client';

import { useEffect, useRef } from 'react';
import '@xterm/xterm/css/xterm.css';

// xterm.js terminal pane. The library touches `window` at import time, so it
// is loaded dynamically inside the effect (this component must stay client-only).
export default function TerminalPane({ onReady }) {
  const containerRef = useRef(null);
  const onReadyRef = useRef(onReady);
  onReadyRef.current = onReady;

  useEffect(() => {
    let term;
    let resizeObserver;
    let cancelled = false;

    (async () => {
      const [{ Terminal }, { FitAddon }] = await Promise.all([
        import('@xterm/xterm'),
        import('@xterm/addon-fit'),
      ]);
      if (cancelled || !containerRef.current) return;

      term = new Terminal({
        convertEol: true,
        cursorBlink: true,
        fontSize: 13,
        fontFamily: '"SF Mono", Menlo, Consolas, monospace',
        theme: {
          background: '#14161c',
          foreground: '#d4d4d4',
          cursor: '#e6b422',
          selectionBackground: '#2c3140',
        },
      });
      const fitAddon = new FitAddon();
      term.loadAddon(fitAddon);
      term.open(containerRef.current);
      fitAddon.fit();

      resizeObserver = new ResizeObserver(() => {
        try { fitAddon.fit(); } catch { /* container hidden */ }
      });
      resizeObserver.observe(containerRef.current);

      onReadyRef.current?.(term);
    })();

    return () => {
      cancelled = true;
      resizeObserver?.disconnect();
      term?.dispose();
    };
  }, []);

  return <div className="terminal" ref={containerRef} />;
}
