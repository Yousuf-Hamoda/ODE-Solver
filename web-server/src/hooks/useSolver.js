import { useState } from 'react'
import { solveODE } from '../api/odeSolver'
import { PRESETS } from '../constants'

/**
 * useSolver
 *
 * Centralises every piece of state and logic the ODE solver needs.
 * Components receive only what they need via props — none of them
 * import this hook directly.
 *
 * Returns an object with:
 *   — input state   : dim, matrix, x0, tEnd
 *   — input setters : setDim, handleMatrixCell, handleX0Cell, setTEnd
 *   — solver state  : result, loading, error
 *   — actions       : solve, applyPreset, evaluateAt
 *   — eval state    : evalT, setEvalT, evalResult
 */
export function useSolver() {
  // ── Input state ───────────────────────────────────────────────────────
  const [dim,    setDimRaw] = useState(2)
  const [matrix, setMatrix] = useState([[0, 1], [-2, -3]])
  const [x0,     setX0]     = useState([1, 0])
  const [tEnd,   setTEnd]   = useState(8)

  // ── Solver output ─────────────────────────────────────────────────────
  const [result,  setResult]  = useState(null)
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState(null)

  // ── Point evaluator ───────────────────────────────────────────────────
  const [evalT,      setEvalT]      = useState('')
  const [evalResult, setEvalResult] = useState(null)

  // ── Helpers ───────────────────────────────────────────────────────────

  /** Change matrix dimension, preserving any existing values. */
  function setDim(newDim) {
    setDimRaw(newDim)
    setMatrix(prev =>
      Array.from({ length: newDim }, (_, i) =>
        Array.from({ length: newDim }, (_, j) => prev[i]?.[j] ?? 0)
      )
    )
    setX0(prev =>
      Array.from({ length: newDim }, (_, i) => prev[i] ?? 0)
    )
    resetOutput()
  }

  /** Update a single cell in matrix A. */
  function handleMatrixCell(row, col, raw) {
    setMatrix(prev => {
      const next = prev.map(r => [...r])
      next[row][col] = raw === '' ? 0 : parseFloat(raw)
      return next
    })
  }

  /** Update a single entry in x0. */
  function handleX0Cell(index, raw) {
    setX0(prev => {
      const next = [...prev]
      next[index] = raw === '' ? 0 : parseFloat(raw)
      return next
    })
  }

  function resetOutput() {
    setResult(null)
    setError(null)
    setEvalResult(null)
    setEvalT('')
  }

  // ── Actions ───────────────────────────────────────────────────────────

  /** Call the Python backend and store the solution. */
  async function solve() {
    setLoading(true)
    resetOutput()
    try {
      const data = await solveODE({ matrix, x0, tEnd: parseFloat(tEnd) || 10 })
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  /** Load a preset system into the inputs. */
  function applyPreset(preset) {
    const n = preset.A.length
    setDimRaw(n)
    setMatrix(preset.A.map(row => [...row]))
    setX0([...preset.x0])
    resetOutput()
  }

  /**
   * Find the closest time sample to `evalT` and store the x values.
   * Uses linear indexing rather than a full search loop.
   */
  function evaluateAt() {
    if (!result || evalT === '') return
    const t = parseFloat(evalT)
    if (isNaN(t)) return

    const { t: ts, x } = result
    const dt  = ts[1] - ts[0]
    const idx = Math.max(0, Math.min(Math.round((t - ts[0]) / dt), ts.length - 1))
    setEvalResult({ t: ts[idx], x: x[idx] })
  }

  return {
    // input state
    dim, matrix, x0, tEnd,
    // input setters
    setDim, handleMatrixCell, handleX0Cell, setTEnd,
    // solver output
    result, loading, error,
    // actions
    solve, applyPreset,
    // point evaluator
    evalT, setEvalT, evalResult, evaluateAt,
    // presets (convenient to pass down)
    presets: PRESETS,
  }
}
