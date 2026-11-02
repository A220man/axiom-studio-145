import HealthStatus from './components/HealthStatus'
import SkillList from './components/SkillList'
import './App.css'

function App() {
  return (
    <div className="app">
      <header>
        <h1>Axiom Studio 145</h1>
        <p>The agent harness performance optimization system</p>
      </header>
      <main>
        <HealthStatus />
        <SkillList />
      </main>
    </div>
  )
}

export default App
