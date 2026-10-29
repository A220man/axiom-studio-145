import { useEffect, useState } from 'react'

interface HealthResponse {
  status: string
}

export default function HealthStatus() {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchHealth() {
      try {
        const response = await fetch('/api/health')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        setHealth(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchHealth()
    const interval = setInterval(fetchHealth, 10000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return <div className="health-status loading">Checking backend health...</div>
  }

  if (error) {
    return <div className="health-status error">Error: {error}</div>
  }

  return (
    <div className="health-status">
      <span className={`status-indicator ${health?.status === 'ok' ? 'healthy' : 'unhealthy'}`}></span>
      <span>Backend Status: {health?.status?.toUpperCase() || 'UNKNOWN'}</span>
    </div>
  )
}
