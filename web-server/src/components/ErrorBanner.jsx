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
        background: 'rgba(220, 38, 38, 0.06)',
        border: '1px solid rgba(220, 38, 38, 0.25)',
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
