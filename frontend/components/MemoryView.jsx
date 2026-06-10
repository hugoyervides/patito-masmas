'use client';

// Live view of the VM's virtual memory during a debug session. The VM sends
// a full snapshot after every quadruple, so this is always scope-accurate
// (function calls swap the local/temporal segments wholesale).
const SEGMENT_ORDER = [
  { key: 'global', label: 'Global', className: 'seg-global' },
  { key: 'local', label: 'Local', className: 'seg-local' },
  { key: 'temporal', label: 'Temporal', className: 'seg-temp' },
  { key: 'pointers', label: 'Apuntadores', className: 'seg-ptr' },
  { key: 'constant', label: 'Constantes', className: 'seg-const' },
];

function formatValue(value) {
  if (value === null || value === undefined) return '—';
  if (typeof value === 'string') return `"${value}"`;
  if (typeof value === 'boolean') return value ? 'true' : 'false';
  return String(value);
}

export default function MemoryView({ memory, changedAddresses, step }) {
  const segments = SEGMENT_ORDER.filter(
    (segment) => memory && memory[segment.key] && Object.keys(memory[segment.key]).length > 0,
  );

  if (segments.length === 0) {
    return (
      <div className="quads-empty">
        Inicia una sesion de depuracion para ver la memoria virtual en vivo.
      </div>
    );
  }

  return (
    <div className="memory">
      {segments.map((segment) => (
        <div key={segment.key}>
          <h3 className="quads-subtitle">{segment.label}</h3>
          <table className="quads-table">
            <thead>
              <tr>
                <th>Direccion</th>
                <th>Valor</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(memory[segment.key])
                .sort((a, b) => Number(a[0]) - Number(b[0]))
                .map(([address, value]) => {
                  const changed = changedAddresses.has(Number(address));
                  return (
                    // Changed rows get a step-scoped key so the flash
                    // animation retriggers even on consecutive writes
                    <tr
                      key={changed ? `${address}-${step}` : address}
                      className={changed ? 'mem-changed' : ''}
                    >
                      <td><span className={`quad-addr ${segment.className}`}>{address}</span></td>
                      <td className="mem-value">{formatValue(value)}</td>
                    </tr>
                  );
                })}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
}
