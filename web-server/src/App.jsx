import React from 'react'
import { useSolver } from './hooks/useSolver'

import Header            from './components/Header'
import PresetBar         from './components/PresetBar'
import MatrixInput       from './components/MatrixInput'
import InitialConditions from './components/InitialConditions'
import SolveButton       from './components/SolveButton'
import ErrorBanner       from './components/ErrorBanner'
import SolutionChart     from './components/SolutionChart'
import EigenPanel        from './components/EigenPanel'
import PointEvaluator    from './components/PointEvaluator'

/**
 * App
 * Root layout component.
 * All state lives in useSolver(); App just wires props to components.
 */
export default function App() {
  const solver = useSolver()

  return (
    <main style={{ maxWidth: 780, margin: '0 auto', padding: '32px 20px' }}>
      <Header />

      <PresetBar
        presets={solver.presets}
        onSelect={solver.applyPreset}
      />

      {/* Inputs: matrix + initial conditions side by side */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 20 }}>
        <MatrixInput
          n={solver.dim}
          matrix={solver.matrix}
          onChange={solver.handleMatrixCell}
          onDimChange={solver.setDim}
        />
        <InitialConditions
          dim={solver.dim}
          x0={solver.x0}
          tEnd={solver.tEnd}
          onX0Change={solver.handleX0Cell}
          onTEndChange={solver.setTEnd}
        />
      </div>

      <SolveButton
        onClick={solver.solve}
        loading={solver.loading}
      />

      <ErrorBanner message={solver.error} />

      {/* Results — only shown after a successful solve */}
      {solver.result && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          <SolutionChart
            result={solver.result}
            dim={solver.dim}
          />
          <EigenPanel
            eigenvalues={solver.result.eigenvalues}
            eigenvectors={solver.result.eigenvectors}
          />
          <PointEvaluator
            evalT={solver.evalT}
            setEvalT={solver.setEvalT}
            evalResult={solver.evalResult}
            onEvaluate={solver.evaluateAt}
            dim={solver.dim}
          />
        </div>
      )}
    </main>
  )
}
