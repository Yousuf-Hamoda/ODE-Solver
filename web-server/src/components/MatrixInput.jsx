import React from 'react'

/**
 * MatrixInput
 * Renders an n×n grid of number inputs for matrix A.
 *
 * Props:
 *   n        — dimension of the matrix
 *   matrix   — number[][] current values
 *   onChange — (row, col, rawValue) => void
 *   onDimChange — (newDim: number) => void
 */
export default function MatrixInput({ n, matrix, onChange, onDimChange }) {
  return (
    <div style={{
      background: 'var(--surface)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius-lg)',
      padding: 18,
    }}>
      {/* Card header: label + dimension selector */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
        <span style={{ fontFamily: 'var(--mono)', fontSize: 12, color: 'var(--accent)', fontWeight: 500 }}>
          Matrix A
        </span>
        <select value={n} onChange={(e) => onDimChange(parseInt(e.target.value))}>
          {[2, 3, 4].map((d) => (
            <option key={d} value={d}>{d}×{d}</option>
          ))}
        </select>
      </div>

      {/* n×n input grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${n}, 1fr)`,
        gap: 6,
      }}>
        {Array.from({ length: n }, (_, row) =>
          Array.from({ length: n }, (_, col) => (
            <input
              key={`${row}-${col}`}
              type="number"
              step="any"
              value={matrix[row]?.[col] ?? 0}
              onChange={(e) => onChange(row, col, e.target.value)}
              style={{ textAlign: 'center' }}
              aria-label={`A[${row + 1}][${col + 1}]`}
            />
          ))
        )}
      </div>
    </div>
  )
}
