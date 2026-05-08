/**
 * Round a float to `digits` significant decimal places,
 * stripping trailing zeros and returning '0' for near-zero values.
 *
 * @param {number} value
 * @param {number} [digits=4]
 * @returns {string}
 */
export function formatNumber(value, digits = 4) {
  if (Math.abs(value) < 1e-10) return '0'
  return parseFloat(value.toFixed(digits)).toString()
}

/**
 * Format a complex number object { re, im } as a human-readable string.
 * Examples:  3.14  |  2i  |  1.5 + 2i  |  1.5 − 2i
 *
 * @param {{ re: number, im: number }} complex
 * @returns {string}
 */
export function formatComplex({ re, im }) {
  const reStr   = formatNumber(re, 4)
  const imAbs   = formatNumber(Math.abs(im), 4)
  const sign    = im < -1e-10 ? '−' : '+'
  const pureIm  = Math.abs(im) > 1e-8
  const pureRe  = Math.abs(re) > 1e-8

  if (!pureIm)  return reStr          // purely real
  if (!pureRe)  return `${formatNumber(im, 4)}i`  // purely imaginary
  return `${reStr} ${sign} ${imAbs}i` // general complex
}
