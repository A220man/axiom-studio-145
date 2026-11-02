import { useEffect, useState } from 'react'

interface Skill {
  id: string
  name: string
  description: string
  category: string
  tags: string[]
  created_at: string
  updated_at: string
}

interface SkillListResponse {
  skills: Skill[]
  total: number
}

interface SkillFormData {
  name: string
  description: string
  category: string
  tags: string
}

export default function SkillList() {
  const [skills, setSkills] = useState<Skill[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showForm, setShowForm] = useState(false)
  const [editingSkill, setEditingSkill] = useState<Skill | null>(null)
  const [formData, setFormData] = useState<SkillFormData>({
    name: '',
    description: '',
    category: '',
    tags: ''
  })

  const fetchSkills = async () => {
    try {
      const response = await fetch('/api/skills')
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data: SkillListResponse = await response.json()
      setSkills(data.skills)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchSkills()
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    
    const tags = formData.tags.split(',').map(t => t.trim()).filter(t => t)
    const skillData = {
      name: formData.name,
      description: formData.description,
      category: formData.category,
      tags
    }

    try {
      let response: Response
      if (editingSkill) {
        response = await fetch(`/api/skills/${editingSkill.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(skillData)
        })
      } else {
        response = await fetch('/api/skills', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(skillData)
        })
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      setShowForm(false)
      setEditingSkill(null)
      setFormData({ name: '', description: '', category: '', tags: '' })
      await fetchSkills()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    }
  }

  const handleEdit = (skill: Skill) => {
    setEditingSkill(skill)
    setFormData({
      name: skill.name,
      description: skill.description,
      category: skill.category,
      tags: skill.tags.join(', ')
    })
    setShowForm(true)
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this skill?')) return
    
    try {
      const response = await fetch(`/api/skills/${id}`, {
        method: 'DELETE'
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      await fetchSkills()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    }
  }

  const handleCancel = () => {
    setShowForm(false)
    setEditingSkill(null)
    setFormData({ name: '', description: '', category: '', tags: '' })
  }

  if (loading) {
    return <div className="skill-list loading">Loading skills...</div>
  }

  if (error) {
    return <div className="skill-list error">Error: {error}</div>
  }

  return (
    <div className="skill-list">
      <div className="skill-list-header">
        <h2>Skills</h2>
        <button className="btn-primary" onClick={() => setShowForm(true)}>
          {editingSkill ? 'Add New Skill' : 'Add Skill'}
        </button>
      </div>

      {showForm && (
        <div className="skill-form-overlay" onClick={handleCancel}>
          <form className="skill-form" onSubmit={handleSubmit} onClick={e => e.stopPropagation()}>
            <h3>{editingSkill ? 'Edit Skill' : 'Create Skill'}</h3>
            <div className="form-group">
              <label htmlFor="name">Name *</label>
              <input
                type="text"
                id="name"
                value={formData.name}
                onChange={e => setFormData({ ...formData, name: e.target.value })}
                required
                maxLength={100}
              />
            </div>
            <div className="form-group">
              <label htmlFor="description">Description</label>
              <textarea
                id="description"
                value={formData.description}
                onChange={e => setFormData({ ...formData, description: e.target.value })}
                maxLength={500}
                rows={3}
              />
            </div>
            <div className="form-group">
              <label htmlFor="category">Category *</label>
              <input
                type="text"
                id="category"
                value={formData.category}
                onChange={e => setFormData({ ...formData, category: e.target.value })}
                required
                maxLength={50}
              />
            </div>
            <div className="form-group">
              <label htmlFor="tags">Tags (comma-separated)</label>
              <input
                type="text"
                id="tags"
                value={formData.tags}
                onChange={e => setFormData({ ...formData, tags: e.target.value })}
                placeholder="python, backend, api"
              />
            </div>
            <div className="form-actions">
              <button type="submit" className="btn-primary">
                {editingSkill ? 'Update' : 'Create'}
              </button>
              <button type="button" className="btn-secondary" onClick={handleCancel}>
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {skills.length === 0 ? (
        <div className="skill-empty">
          <p>No skills yet. Click "Add Skill" to create your first skill.</p>
        </div>
      ) : (
        <ul className="skill-items">
          {skills.map(skill => (
            <li key={skill.id} className="skill-item">
              <div className="skill-info">
                <div className="skill-header">
                  <h3>{skill.name}</h3>
                  <span className="skill-category">{skill.category}</span>
                </div>
                <p className="skill-description">{skill.description || 'No description'}</p>
                <div className="skill-tags">
                  {skill.tags.map(tag => (
                    <span key={tag} className="skill-tag">{tag}</span>
                  ))}
                </div>
              </div>
              <div className="skill-actions">
                <button className="btn-secondary" onClick={() => handleEdit(skill)}>Edit</button>
                <button className="btn-danger" onClick={() => handleDelete(skill.id)}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
