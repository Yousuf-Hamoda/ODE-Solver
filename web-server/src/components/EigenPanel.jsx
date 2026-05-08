import React from 'react'
import { SERIES_COLORS } from '../constants'
import { formatComplex } from '../utils/format'

/**
 * EigenCard
 * Renders a single eigenvalue + its eigenvector in a colored card.
 *
 * Props:
 *   index       — 0-based index (used for color + label)
 *   eigenvalue  — { re, im }
 *   eigenvector — [{ re, im }, ...]
 */
function EigenCard({ index, eigenvalue, eigenvector }) {
  const color = SERIES_COLORS[index % SERIES_COLORS.length]

  return (
    <div style={{
      background: 'var(--surface2)',
      border: '1px solid var(--border)',
      borderLeft: `3px solid ${color}`,
      borderRadius: 'var(--radius-md)',
      padding: '12px 14px',
      marginBottom: 8,
    }}>
      {/* Eigenvalue row */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 6 }}>
        <span style={{ fontFamily: 'var(--mono)', fontSize: 12, color: 'var(--muted)' }}>
          λ{index + 1}
        </span>
        <span style={{ fontFamily: 'var(--mono)', fontSize: 14, color, fontWeight: 500 }}>
          {formatComplex(eigenvalue)}
        </span>
      </div>

      {/* Eigenvector row */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        <span style={{ fontFamily: 'var(--mono)', fontSize: 11, color: 'var(--muted)' }}>v =</span>
        <span style={{ fontFamily: 'var(--mono)', fontSize: 12, color: '#b8bfd0' }}>
          [ {eigenvector.map(formatComplex).join(', ')} ]
        </span>
      </div>
    </div>
  )
}

/**
 * EigenPanel
 * Container card that renders one EigenCard per eigenvalue.
 *
 * Props:
 *   eigenvalues  — [{ re, im }, ...]
 *   eigenvectors — [[{ re, im }, ...], ...]
 */
export default function EigenPanel({ eigenvalues, eigenvectors }) {
  return (
    <div style={{
      background: 'var(--surface)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius-lg)',
      padding: 20,
    }}>
      <p style={{ fontFamily: 'var(--mono)', fontSize: 12, color: 'var(--accent)', fontWeight: 500, marginBottom: 12 }}>
        Eigenvalues &amp; Eigenvectors
      </p>

      {eigenvalues.map((lam, i) => (
        <EigenCard
          key={i}
          index={i}
          eigenvalue={lam}
          eigenvector={eigenvectors[i]}
        />
      ))}
    </div>
  )
}
