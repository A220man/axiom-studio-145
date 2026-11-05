import { useEffect, useState } from 'react'

interface Condition {
  field: string
  operator: string
  value: any
}

interface Action {
  type: string
  parameters: Record<string, any>
}

interface Instinct {
  id: string
  name: string
  description: string
  conditions: Condition[]
  actions: Action[]
  priority: number
  enabled: boolean
  created_at: string
  updated_at: string
}

interface InstinctListResponse {
  instincts: Instinct[]
  total: number
}

interface EvaluationResult {
  instinct_id: string
  instinct_name: string
  matched: boolean
  executed_actions: any[]
  timestamp: string
}

interface EvaluationResponse {
  results: EvaluationResult[]
  total_evaluated: number
  total_matched: number
}

interface InstinctFormData {
  name: string
  description: string
  conditions: string
  actions: string
  priority: string
  enabled: string
}

const OPERATORS = [
  'equals',
  'not_equals',
  'contains',
  'greater_than',
  'less_than',
  'in',
  'not_in'
]

const ACTION_TYPES = [
  'log',
  'notify',
  'execute',
  'store_memory',
  'skip'
]

export default function InstinctList() {
  const [instincts, setInstincts] = useState<Instinct[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showForm, setShowForm] = useState(false)
  const [editingInstinct, setEditingInstinct] = useState<Instinct | null>(null)
  const [formData, setFormData] = useState<InstinctFormData>({
    name: '',
    description: '',
    conditions: '[]',
    actions: '[]',
    priority: '0',
    enabled: 'true'
  })
  const [evalData, setEvalData] = useState('{}')
  const [evalResult, setEvalResult] = useState<EvaluationResponse | null>(null)
  const [evalLoading, setEvalLoading] = useState(false)

  const fetchInstincts = async () => {
    try {
      const response = await fetch('/api/instincts')
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data: InstinctListResponse = await response.json()
      setInstincts(data.instincts)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchInstincts()
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    
    let conditions: Condition[] = []
    let actions: Action[] = []
    
    try {
      conditions = JSON.parse(formData.conditions)
      actions = JSON.parse(formData.actions)
    } catch {
      setError('Invalid JSON in conditions or actions')
      return
    }

    const instinctData = {
      name: formData.name,
      description: formData.description,
      conditions,
      actions,
      priority: parseInt(formData.priority, 10) || 0,
      enabled: formData.enabled === 'true'
    }

    try {
      let response: Response
      if (editingInstinct) {
        response = await fetch(`/api/instincts/${editingInstinct.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(instinctData)
        })
      } else {
        response = await fetch('/api/instincts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(instinctData)
        })
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      setShowForm(false)
      setEditingInstinct(null)
      setFormData({ name: '', description: '', conditions: '[]', actions: '[]', priority: '0', enabled: 'true' })
      await fetchInstincts()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    }
  }

  const handleEdit = (instinct: Instinct) => {
    setEditingInstinct(instinct)
    setFormData({
      name: instinct.name,
      description: instinct.description,
      conditions: JSON.stringify(instinct.conditions, null, 2),
      actions: JSON.stringify(instinct.actions, null, 2),
      priority: instinct.priority.toString(),
      enabled: instinct.enabled.toString()
    })
    setShowForm(true)
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this instinct?')) return
    
    try {
      const response = await fetch(`/api/instincts/${id}`, {
        method: 'DELETE'
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      await fetchInstincts()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    }
  }

  const handleCancel = () => {
    setShowForm(false)
    setEditingInstinct(null)
    setFormData({ name: '', description: '', conditions: '[]', actions: '[]', priority: '0', enabled: 'true' })
  }

  const handleEvaluate = async (e: React.FormEvent) => {
    e.preventDefault()
    setEvalResult(null)
    setEvalLoading(true)
    
    let data: Record<string, any> = {}
    try {
      data = JSON.parse(evalData)
    } catch {
      setError('Invalid JSON in evaluation data')
      setEvalLoading(false)
      return
    }

    try {
      const response = await fetch('/api/instincts/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data })
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const result: EvaluationResponse = await response.json()
      setEvalResult(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setEvalLoading(false)
    }
  }

  if (loading) {
    return <div className="instinct-list loading">Loading instincts...</div>
  }

  if (error) {
    return <div className="instinct-list error">Error: {error}</div>
  }

  return (
    <div className="instinct-list">
      <div className="instinct-list-header">
        <h2>Instincts</h2>
        <button className="btn-primary" onClick={() => setShowForm(true)}>
          {editingInstinct ? 'Edit Instinct' : 'Create Instinct'}
        </button>
      </div>

      {/* Instinct Form */}
      {showForm && (
        <div className="instinct-form-overlay">
          <div className="instinct-form">
            <h3>{editingInstinct ? 'Edit Instinct' : 'Create Instinct'}</h3>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="name">Name *</label>
                <input
                  id="name"
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                  maxLength={100}
                />
              </div>

              <div className="form-group">
                <label htmlFor="description">Description</label>
                <textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  maxLength={500}
                  rows={3}
                />
              </div>

              <div className="form-group">
                <label htmlFor="priority">Priority (0-100)</label>
                <input
                  id="priority"
                  type="number"
                  value={formData.priority}
                  onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                  min={0}
                  max={100}
                />
              </div>

              <div className="form-group">
                <label>
                  <input
                    type="checkbox"
                    checked={formData.enabled === 'true'}
                    onChange={(e) => setFormData({ ...formData, enabled: e.target.checked.toString() })}
                  />
                  Enabled
                </label>
              </div>

              <div className="form-group">
                <label htmlFor="conditions">Conditions (JSON Array)</label>
                <textarea
                  id="conditions"
                  value={formData.conditions}
                  onChange={(e) => setFormData({ ...formData, conditions: e.target.value })}
                  rows={6}
                  placeholder={JSON.stringify([
                    { field: 'level', operator: 'equals', value: 'error' }
                  ], null, 2)}
                />
                <small>Operators: {OPERATORS.join(', ')}</small>
              </div>

              <div className="form-group">
                <label htmlFor="actions">Actions (JSON Array)</label>
                <textarea
                  id="actions"
                  value={formData.actions}
                  onChange={(e) => setFormData({ ...formData, actions: e.target.value })}
                  rows={6}
                  placeholder={JSON.stringify([
                    { type: 'log', parameters: { message: 'Error detected' } }
                  ], null, 2)}
                />
                <small>Action types: {ACTION_TYPES.join(', ')}</small>
              </div>

              <div className="form-actions">
                <button type="submit" className="btn-primary">
                  {editingInstinct ? 'Update' : 'Create'}
                </button>
                <button type="button" className="btn-secondary" onClick={handleCancel}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Instinct List */}
      <div className="instinct-table-container">
        <table className="instinct-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Conditions</th>
              <th>Actions</th>
              <th>Priority</th>
              <th>Enabled</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {instincts.map((instinct) => (
              <tr key={instinct.id}>
                <td>{instinct.name}</td>
                <td>{instinct.description || '-'}</td>
                <td>
                  <pre>{JSON.stringify(instinct.conditions, null, 2)}</pre>
                </td>
                <td>
                  <pre>{JSON.stringify(instinct.actions, null, 2)}</pre>
                </td>
                <td>{instinct.priority}</td>
                <td>{instinct.enabled ? 'Yes' : 'No'}</td>
                <td>
                  <button className="btn-secondary btn-sm" onClick={() => handleEdit(instinct)}>Edit</button>
                  <button className="btn-danger btn-sm" onClick={() => handleDelete(instinct.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {instincts.length === 0 && (
          <div className="empty-state">No instincts yet. Create one to get started.</div>
        )}
      </div>

      {/* Evaluation Panel */}
      <div className="evaluation-panel">
        <h3>Evaluate Instincts</h3>
        <form onSubmit={handleEvaluate}>
          <div className="form-group">
            <label htmlFor="evalData">Context Data (JSON)</label>
            <textarea
              id="evalData"
              value={evalData}
              onChange={(e) => setEvalData(e.target.value)}
              rows={4}
              placeholder={JSON.stringify({ level: 'error', message: 'Something went wrong' }, null, 2)}
            />
          </div>
          <button type="submit" className="btn-primary" disabled={evalLoading}>
            {evalLoading ? 'Evaluating...' : 'Evaluate'}
          </button>
        </form>

        {evalResult && (
          <div className="evaluation-results">
            <h4>Results</h4>
            <p>Total evaluated: {evalResult.total_evaluated} | Matched: {evalResult.total_matched}</p>
            <div className="results-list">
              {evalResult.results.map((result, idx) => (
                <div key={idx} className={`result-item ${result.matched ? 'matched' : 'not-matched'}`}>
                  <div className="result-header">
                    <strong>{result.instinct_name}</strong>
                    <span className={result.matched ? 'badge-matched' : 'badge-not-matched'}>
                      {result.matched ? 'MATCHED' : 'NO MATCH'}
                    </span>
                  </div>
                  {result.executed_actions.length > 0 && (
                    <div className="executed-actions">
                      <strong>Executed Actions:</strong>
                      <ul>
                        {result.executed_actions.map((action, i) => (
                          <li key={i}>{JSON.stringify(action)}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
