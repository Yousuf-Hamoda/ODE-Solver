import React from 'react'
import { SERIES_COLORS } from '../constants'
import { formatNumber } from '../utils/format'

/**
 * PointEvaluator
 * Lets the user type a time value and see the solution vector at that point.
 * Nearest sample in the precomputed solution is used.
 *
 * Props:
 *   evalT       — string, the current input value
 *   setEvalT    — (string) => void
 *   evalResult  — null | { t: number, x: number[] }
 *   onEvaluate  — () => void, triggered on button click
 *   dim         — number of state variables
 */
export default function PointEvaluator({ evalT, setEvalT, evalResult, onEvaluate, dim }) {
  return (
    <div style={{
      background: 'var(--surface)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius-lg)',
      padding: 20,
      boxShadow: 'var(--shadow-sm)',
    }}>
      <p style={{ fontFamily: 'var(--mono)', fontSize: 12, color: 'var(--accent)', fontWeight: 500, marginBottom: 12 }}>
        Evaluate at t
      </p>

      {/* Input row */}
      <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
        <input
          type="number"
          step="any"
          placeholder="e.g. 2.5"
          value={evalT}
          onChange={(e) => setEvalT(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && onEvaluate()}
          style={{ maxWidth: 120 }}
          aria-label="Time value to evaluate"
        />
        <button
          onClick={onEvaluate}
          style={{
            background: 'var(--surface2)',
            border: '1px solid var(--border2)',
            color: 'var(--text)',
            borderRadius: 'var(--radius-sm)',
            padding: '7px 16px',
            fontSize: 14,
          }}
        >
          Evaluate
        </button>
      </div>

      {/* Results */}
      {evalResult && (
        <div style={{ marginTop: 14, fontFamily: 'var(--mono)', fontSize: 13 }}>
          <span style={{ color: 'var(--muted)' }}>
            t ≈ {formatNumber(evalResult.t, 4)}
          </span>

          <div style={{ display: 'flex', gap: 20, marginTop: 6, flexWrap: 'wrap' }}>
            {evalResult.x.map((value, i) => (
              <div key={i}>
                <span style={{ color: 'var(--muted)' }}>x{i + 1} = </span>
                <span style={{ color: SERIES_COLORS[i % SERIES_COLORS.length], fontWeight: 500 }}>
                  {formatNumber(value, 6)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
