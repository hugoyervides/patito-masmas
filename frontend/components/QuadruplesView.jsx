'use client';

import { useEffect, useMemo, useRef } from 'react';

// Virtual memory layout of the Patito ++ compiler (see data_structures/vm_memory.py)
const SEGMENTS = [
  { name: 'Global', from: 1000, to: 7999, className: 'seg-global' },
  { name: 'Local', from: 8000, to: 14999, className: 'seg-local' },
  { name: 'Constante', from: 15000, to: 19999, className: 'seg-const' },
  { name: 'Temporal', from: 20000, to: 29999, className: 'seg-temp' },
  { name: 'Apuntador', from: 30000, to: 40000, className: 'seg-ptr' },
];

// Operators whose `result` is a jump target (a quadruple number, not an address)
const JUMP_OPERATORS = new Set(['GOTO', 'GOTOF', 'GOSUB']);

function segmentFor(address) {
  return SEGMENTS.find((segment) => address >= segment.from && address <= segment.to);
}

function formatConstant(value) {
  return typeof value === 'string' ? `"${value}"` : String(value);
}

function Operand({ value, constantsByAddress }) {
  if (value === null || value === undefined) {
    return <span className="quad-empty">—</span>;
  }
  if (typeof value === 'number') {
    const segment = segmentFor(value);
    if (segment) {
      const constant = constantsByAddress.get(value);
      const title = constant !== undefined
        ? `Direccion ${value} · segmento ${segment.name.toLowerCase()} · valor ${formatConstant(constant)}`
        : `Direccion ${value} · segmento ${segment.name.toLowerCase()}`;
      return (
        <span className={`quad-addr ${segment.className}`} title={title}>
          {value}
          {constant !== undefined && (
            <span className="quad-const-value"> {formatConstant(constant)}</span>
          )}
        </span>
      );
    }
    return <span>{value}</span>;
  }
  if (typeof value === 'object') {
    return <span className="quad-obj">{JSON.stringify(value)}</span>;
  }
  return <span className="quad-name">{String(value)}</span>;
}

export default function QuadruplesView({ quadruples, constants, currentQuad = null, onSelectLine = null }) {
  const constantsByAddress = useMemo(
    () => new Map(constants.map((entry) => [entry.v_address, entry.constant])),
    [constants],
  );

  //Keep the instruction about to execute visible while debugging
  const currentRowRef = useRef(null);
  useEffect(() => {
    currentRowRef.current?.scrollIntoView({ block: 'nearest' });
  }, [currentQuad]);

  if (!quadruples.length) {
    return (
      <div className="quads-empty">
        Compila o ejecuta un programa para ver los cuadruplos que genera el compilador.
      </div>
    );
  }

  return (
    <div className="quads">
      <div className="quads-legend">
        {SEGMENTS.map((segment) => (
          <span key={segment.name} className={`legend-chip ${segment.className}`}>
            {segment.name} {segment.from}–{segment.to}
          </span>
        ))}
      </div>

      <table className="quads-table">
        <thead>
          <tr>
            <th>#</th>
            <th title="Linea de codigo fuente">Lin</th>
            <th>Operador</th>
            <th>Op. izq</th>
            <th>Op. der</th>
            <th>Resultado</th>
          </tr>
        </thead>
        <tbody>
          {quadruples.map((quad, index) => (
            <tr
              key={index}
              ref={index === currentQuad ? currentRowRef : null}
              className={`${index === currentQuad ? 'quad-current' : ''}${quad.line && onSelectLine ? ' quad-clickable' : ''}`}
              title={quad.line ? `Click para ir a la linea ${quad.line} en el editor` : undefined}
              onClick={() => quad.line && onSelectLine && onSelectLine(quad.line)}
            >
              <td className="quad-no">{index === currentQuad ? '▶ ' : ''}{index}</td>
              <td className="quad-line">{quad.line ?? '—'}</td>
              <td className="quad-op">{quad.operator}</td>
              <td><Operand value={quad.l_operand} constantsByAddress={constantsByAddress} /></td>
              <td><Operand value={quad.r_operand} constantsByAddress={constantsByAddress} /></td>
              <td>
                {JUMP_OPERATORS.has(quad.operator) && typeof quad.result === 'number' ? (
                  <span className="quad-jump" title={`Salta al cuadruplo ${quad.result}`}>
                    → {quad.result}
                  </span>
                ) : (
                  <Operand value={quad.result} constantsByAddress={constantsByAddress} />
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {constants.length > 0 && (
        <>
          <h3 className="quads-subtitle">Tabla de constantes</h3>
          <table className="quads-table">
            <thead>
              <tr>
                <th>Direccion</th>
                <th>Tipo</th>
                <th>Valor</th>
              </tr>
            </thead>
            <tbody>
              {constants.map((entry) => (
                <tr key={entry.v_address}>
                  <td><span className="quad-addr seg-const">{entry.v_address}</span></td>
                  <td>{entry.type}</td>
                  <td className="quad-const-value">{formatConstant(entry.constant)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}
