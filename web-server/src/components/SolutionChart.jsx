import React, { useRef, useEffect } from 'react'
import Chart from 'chart.js/auto'
import { SERIES_COLORS } from '../constants'
import { formatNumber } from '../utils/format'

/**
 * SolutionChart
 * Renders the x(t) solution as a multi-series line chart using Chart.js.
 * Destroys and recreates the chart whenever `result` changes.
 *
 * Props:
 *   result — { t: number[], x: number[][] } from the solver API
 *   dim    — number of state variables (sets number of series)
 */
export default function SolutionChart({ result, dim }) {
  const canvasRef = useRef(null)
  const chartRef  = useRef(null)

  useEffect(() => {
    if (!result || !canvasRef.current) return

    // Destroy any previous chart instance before creating a new one
    if (chartRef.current) chartRef.current.destroy()

    const { t, x } = result

    const datasets = Array.from({ length: dim }, (_, i) => ({
      label: `x${i + 1}(t)`,
      data: t.map((tv, ti) => ({ x: tv, y: x[ti][i] })),
      borderColor: SERIES_COLORS[i % SERIES_COLORS.length],
      borderWidth: 2,
      pointRadius: 0,
      tension: 0.3,
      fill: false,
    }))

    chartRef.current = new Chart(canvasRef.current, {
      type: 'line',
      data: { datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 600, easing: 'easeOutQuart' },
        plugins: {
          legend: { display: false }, // we draw our own legend below
          tooltip: {
            mode: 'index',
            intersect: false,
            backgroundColor: '#1c2030',
            borderColor: 'rgba(255,255,255,0.1)',
            borderWidth: 1,
            titleColor: '#7c8099',
            bodyColor: '#e8eaf0',
            titleFont: { family: 'DM Mono' },
            bodyFont:  { family: 'DM Mono' },
            callbacks: {
              label: (ctx) => ` x${ctx.datasetIndex + 1} = ${formatNumber(ctx.parsed.y, 5)}`,
            },
          },
        },
        scales: {
          x: {
            type: 'linear',
            title: { display: true, text: 't', color: '#7c8099', font: { family: 'DM Mono' } },
            grid:  { color: 'rgba(255,255,255,0.04)' },
            ticks: { color: '#7c8099', font: { family: 'DM Mono', size: 11 } },
          },
          y: {
            title: { display: true, text: 'x(t)', color: '#7c8099', font: { family: 'DM Mono' } },
            grid:  { color: 'rgba(255,255,255,0.04)' },
            ticks: { color: '#7c8099', font: { family: 'DM Mono', size: 11 } },
          },
        },
      },
    })

    return () => {
      if (chartRef.current) chartRef.current.destroy()
    }
  }, [result, dim])

  return (
    <div style={{
      background: 'var(--surface)',
      border: '1px solid var(--border)',
      borderRadius: 'var(--radius-lg)',
      padding: 20,
    }}>
      {/* Card header */}
      <p style={{ fontFamily: 'var(--mono)', fontSize: 12, color: 'var(--accent)', fontWeight: 500, marginBottom: 4 }}>
        Solution x(t)
      </p>

      {/* Color legend — one swatch per series */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 14, marginTop: 10 }}>
        {Array.from({ length: dim }, (_, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 13, color: 'var(--muted)' }}>
            <span style={{
              width: 18,
              height: 2,
              background: SERIES_COLORS[i % SERIES_COLORS.length],
              borderRadius: 2,
              display: 'inline-block',
            }} />
            <span style={{ fontFamily: 'var(--mono)' }}>x{i + 1}(t)</span>
          </div>
        ))}
      </div>

      {/* Chart canvas */}
      <div style={{ position: 'relative', width: '100%', height: 280, marginTop: 16 }}>
        <canvas
          ref={canvasRef}
          role="img"
          aria-label={`Line chart of ${dim} state variables over time`}
        />
      </div>
    </div>
  )
}
