import { API_BASE } from '../constants'

/**
 * POST /solve
 *
 * Sends the matrix A, initial conditions x0, and time range to the
 * Python Flask backend.  Returns the parsed JSON response.
 *
 * @param {object} params
 * @param {number[][]} params.matrix   - n×n coefficient matrix A
 * @param {number[]}   params.x0       - initial condition vector
 * @param {number}     params.tEnd     - end time
 * @param {number}     [params.tSteps] - number of time samples (default 300)
 * @returns {Promise<SolverResponse>}
 *
 * @typedef {object} SolverResponse
 * @property {number[]}     t            - time points
 * @property {number[][]}   x            - solution vectors, one per time point
 * @property {Complex[]}    eigenvalues
 * @property {Complex[][]}  eigenvectors
 *
 * @typedef {{ re: number, im: number }} Complex
 */
export async function solveODE({ matrix, x0, tEnd, tSteps = 300 }) {
  const response = await fetch(`${API_BASE}/solve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      matrix,
      x0,
      t_start: 0,
      t_end: tEnd,
      t_steps: tSteps,
    }),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.error || `Server error ${response.status}`)
  }

  return data
}
