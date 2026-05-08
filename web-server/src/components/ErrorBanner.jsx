import React from 'react'

/**
 * ErrorBanner
 * Displays a styled error message when the solver returns an error.
 * Renders nothing if `message` is falsy.
 *
 * Props:
 *   message — string | null
 */
export default function ErrorBanner({ message }) {
  if (!message) return null

  return (
    <div
      role="alert"
      style={{
        background: 'rgba(248, 113, 113, 0.08)',
        border: '1px solid rgba(248, 113, 113, 0.3)',
        borderRadius: 'var(--radius-sm)',
        padding: '12px 14px',
        color: 'var(--danger)',
        fontFamily: 'var(--mono)',
        fontSize: 13,
        marginBottom: 20,
      }}
    >
      {message}
    </div>
  )
}
