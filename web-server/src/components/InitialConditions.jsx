import React from 'react'

/**
 * InitialConditions
 * Renders one number input per state variable for x(0),
 * plus the t_end input.
 *
 * Props:
 *   dim      — number of state variables
 *   x0       — number[] current initial condition values
 *   tEnd     — current end time value
 *   onX0Change  — (index, rawValue) => void
 *   onTEndChange — (rawValue) => void
 */
export default function InitialConditions({ dim, x0, tEnd, onX0Change, onTEndChange }) {
  return (
    <div style={{
      background: 'var(--surface)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius-lg)',
      padding: 18,
    }}>
      <p style={{ fontFamily: 'var(--mono)', fontSize: 12, color: 'var(--accent)', fontWeight: 500, marginBottom: 12 }}>
        Initial conditions x(0)
      </p>

      {/* One row per state variable */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
        {Array.from({ length: dim }, (_, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <span style={{ fontFamily: 'var(--mono)', fontSize: 12, color: 'var(--muted)', minWidth: 30 }}>
              x{i + 1}
            </span>
            <input
              type="number"
              step="any"
              value={x0[i] ?? 0}
              onChange={(e) => onX0Change(i, e.target.value)}
              aria-label={`Initial condition x${i + 1}`}
            />
          </div>
        ))}
      </div>

      {/* End time */}
      <div style={{ marginTop: 14, display: 'flex', alignItems: 'center', gap: 8 }}>
        <span style={{ fontFamily: 'var(--mono)', fontSize: 12, color: 'var(--muted)', minWidth: 30 }}>
          t end
        </span>
        <input
          type="number"
          step="any"
          value={tEnd}
          onChange={(e) => onTEndChange(e.target.value)}
          style={{ maxWidth: 80 }}
          aria-label="End time"
        />
      </div>
    </div>
  )
}
