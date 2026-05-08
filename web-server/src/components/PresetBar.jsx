import React, { useState } from 'react'

/**
 * PresetBar
 * Renders one button per preset system.
 *
 * Props:
 *   presets    — array of { label, A, x0 }
 *   onSelect   — called with the chosen preset object
 */
export default function PresetBar({ presets, onSelect }) {
  const [hovered, setHovered] = useState(null)

  return (
    <div style={{ display: 'flex', gap: 8, marginBottom: 22, flexWrap: 'wrap' }}>
      {presets.map((preset) => (
        <button
          key={preset.label}
          onClick={() => onSelect(preset)}
          onMouseEnter={() => setHovered(preset.label)}
          onMouseLeave={() => setHovered(null)}
          style={{
            background: 'var(--surface2)',
            border: `1px solid ${hovered === preset.label ? 'var(--accent)' : 'var(--border2)'}`,
            color: hovered === preset.label ? 'var(--text)' : 'var(--muted)',
            borderRadius: 'var(--radius-sm)',
            padding: '5px 12px',
            fontSize: 13,
            fontFamily: 'var(--mono)',
            transition: 'border-color 0.15s, color 0.15s',
          }}
        >
          {preset.label}
        </button>
      ))}
    </div>
  )
}
