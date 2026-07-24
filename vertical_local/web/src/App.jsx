import React, {useState, useEffect} from 'react'

export default function App(){
  const [mode, setMode] = useState('intelligence') // 'intelligence' | 'boardroom'
  const [theme, setTheme] = useState('default') // 'default' | 'cyberpunk' | 'ghost' | 'royal'
  const [loading, setLoading] = useState(false)

  // Handle theme changes via body class
  useEffect(() => {
    const body = document.body;
    body.classList.remove('theme-cyberpunk', 'theme-ghost', 'theme-royal');
    if (theme !== 'default') {
      body.classList.add(`theme-${theme}`);
    }
  }, [theme]);

  return (
    <div className="container">
      <header>
        <div className="header-top">
          <h1>Vertical Local — Command Console</h1>
          <div className="status-container">
            <span className="status-pill status-pill-active">System Online</span>
            {/* Easter Egg: Hidden Patron Link */}
            <a 
              href="https://example.com/support" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="patron-link"
              title="Support the Nexus"
            >
              [Patron]
            </a>
          </div>
        </div>
        
        <nav className="mode-switcher">
          <button 
            className={`mode-btn ${mode === 'intelligence' ? 'active' : ''}`}
            onClick={() => setMode('intelligence')}
          >
            Intelligence Interface
          </button>
          <button 
            className={`mode-btn ${mode === 'boardroom' ? 'active' : ''}`}
            onClick={() => setMode('boardroom')}
          >
            Boardroom Engine
          </button>
        </nav>

        {/* Theme Switcher Easter Egg */}
        <div className="theme-switcher" style={{marginTop: '1rem', display: 'flex', gap: '0.5rem'}}>
          <button className="btn-secondary" style={{fontSize: '10px', padding: '2px 8px'}} onClick={() => setTheme('default')}>Default</button>
          <button className="btn-secondary" style={{fontSize: '10px', padding: '2px 8px'}} onClick={() => setTheme('cyberpunk')}>Cyberpunk</button>
          <button className="btn-secondary" style={{fontSize: '10px', padding: '2px 8px'}} onClick={() => setTheme('ghost')}>Ghost</button>
          <button className="btn-secondary" style={{fontSize: '10px', padding: '2px 8px'}} onClick={() => setTheme('royal')}>Royal</button>
        </div>
      </header>

      <main>
        {mode === 'intelligence' ? (
          <IntelligenceView 
            setLoading={setLoading}
            loading={loading}
          />
        ) : (
          <BoardroomView 
            setLoading={setLoading}
            loading={loading}
          />
        )}
      </main>
    </div>
  )
}

// --- Intelligence View Component ---
function IntelligenceView({loading, setLoading}){
  const [provider, setProvider] = useState('openai')
  const [model, setModel] = useState('gpt-4o-mini')
  const [prompt, setPrompt] = useState('')
  const [apiKey, setApiKey] = useState('')
  const [response, setResponse] = useState('')
  const [presets, setPresets] = useState([])
  const [selectedPreset, setSelectedPreset] = useState('')

  useEffect(()=>{ loadPresets() }, [])

  async function loadPresets(){
    try{
      const res = await fetch('/presets')
      const data = await res.json()
      setPresets(Array.isArray(data)?data:[])
    }catch(e){
      console.warn('Could not load presets', e)
    }
  }

  function applyPreset(p){
    setSelectedPreset(p.id)
    setProvider(p.provider || 'openai')
    setModel(p.model || '')
    if(p.prompt_template) setPrompt(p.prompt_template)
  }

  async function savePreset(){
    const name = prompt('Preset name:')
    if(!name) return
    const body = {name, description: '', provider, model, prompt_template: prompt}
    const res = await fetch('/presets', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)})
    if(res.ok){ loadPresets() }
  }

  async function deletePreset(id){
    if(!confirm('Delete preset?')) return
    await fetch('/presets/'+id, {method:'DELETE'})
    loadPresets()
  }

  async function handleGenerate(){
    setLoading(true)
    setResponse('')
    try{
      const res = await fetch('/generate', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({provider, model, prompt, api_key: apiKey})
      })
      const data = await res.json()
      if(!res.ok) throw new Error(data.detail || JSON.stringify(data))
      setResponse(data.text)
    }catch(e){
      setResponse('Error: '+e.message)
    }finally{setLoading(false)}
  }

  return (
    <div className="dashboard-grid">
      <section className="main-controls card">
        <h2>Intelligence Interface</h2>
        
        <div className="controls">
          <label>Provider
            <select value={provider} onChange={e=>setProvider(e.target.value)}>
              <option value="openai">OpenAI</option>
              <option value="hf">HuggingFace</option>
            </select>
          </label>
          <label>Model
            <input value={model} onChange={e=>setModel(e.target.value)} />
          </label>
          <label>API Key (optional)
            <input value={apiKey} onChange={e=>setApiKey(e.target.value)} placeholder="Leave blank to use server env" />
          </label>
        </div>

        <div style={{marginTop: '1.5rem'}}>
          <label>Intelligence Prompt</label>
          <textarea value={prompt} onChange={e=>setPrompt(e.target.value)} placeholder="Enter prompt for the swarm..." rows={8}></textarea>
        </div>
        <div style={{display: 'flex', gap: '1rem', marginTop: '1.5rem'}}>
          <button className="btn-primary" onClick={handleGenerate} disabled={loading}>
            {loading ? <><span className="spinner"></span> Generating...</> : 'Execute Intelligence'}
          </button>
          <button className="btn-secondary" onClick={savePreset}>Save as Preset</button>
        </div>

        <div className="response-area">
          <h2>Intelligence Output</h2>
          <div className="response-text">{response || 'Awaiting execution...'}</div>
        </div>
      </section>

      <aside className="sidebar">
        <div className="card">
          <h3>Intelligence Presets</h3>
          <div className="presets-list">
            {presets.length===0 && <div className="text-secondary">No presets yet</div>}
            {presets.map(p=> (
              <div key={p.id} className="preset-item">
                <span className="preset-item-title">{p.name}</span>
                <div className="preset-item-meta">{p.provider} • {p.model}</div>
                <div className="preset-actions">
                  <button className="btn-secondary" onClick={()=>applyPreset(p)}>Apply</button>
                  <button className="btn-danger" onClick={()=>deletePreset(p.id)}>Delete</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </aside>
    </div>
  )
}

// --- Boardroom View Component ---
function BoardroomView({loading, setLoading}){
  const [caseText, setCaseText] = useState('Summarize strengths/weaknesses of current Vertical AI deployment and recommend product-market fit moves.')
  const [personaIds, setPersonaIds] = useState('')
  const [useThoth, setUseThoth] = useState(false)
  const [useScouts, setUseScouts] = useState(false)
  const [turns, setTurns] = useState(3)
  const [sims, setSims] = useState(25)
  const [report, setReport] = useState('')

  async function runBoardroom(){
    setLoading(true)
    setReport('')
    
    const persona_array = personaIds.trim() ? personaIds.split(',').map(s=>s.trim()) : undefined
    
    const body = { 
      case_text: caseText, 
      persona_ids: persona_array, 
      turns: parseInt(turns || 3, 10), 
      sims: parseInt(sims || 25, 10), 
      use_thoth: useThoth, 
      use_scouts: useScouts 
    };

    try{
      const resp = await fetch('/debate/', {
        method:'POST', 
        headers:{'Content-Type':'application/json'}, 
        body: JSON.stringify(body)
      });
      
      if(!resp.ok){
        const txt = await resp.text();
        setReport('Error: ' + txt);
        return;
      }

      const html = await resp.text();
      setReport(html);
    }catch(e){
      setReport('Network or server error: ' + e.message);
    }finally{
      setLoading(false);
    }
  }

  return (
    <div className="dashboard-grid">
      <section className="main-controls card">
        <h2>Boardroom Engine</h2>
        
        <div className="controls-group" style={{display:'flex', flexDirection:'column', gap: '1.5rem'}}>
          <div className="input-group">
            <label>Case / Brief</label>
            <textarea 
              value={caseText} 
              onChange={e=>setCaseText(e.target.value)} 
              placeholder="Enter the case for the boardroom..."
              rows={6}
            ></textarea>
          </div>

          <div className="input-group">
            <label>Persona IDs (comma separated)</label>
            <input 
              value={personaIds} 
              onChange={e=>setPersonaIds(e.target.value)} 
              placeholder="e.g. p1, p2, p3"
            />
          </div>

          <div className="checkbox-group" style={{display:'flex', gap:'2rem', alignItems:'center'}}>
            <label style={{flexDirection:'row', alignItems:'center', gap:'8px', cursor:'pointer'}}>
              <input type="checkbox" checked={useThoth} onChange={e=>setUseThoth(e.target.checked)} />
              Use Thoth
            </label>
            <label style={{flexDirection:'row', alignItems:'center', gap:'8px', cursor:'pointer'}}>
              <input type="checkbox" checked={useScouts} onChange={e=>setUseScouts(e.target.checked)} />
              Use Swarm Scouts
            </label>
          </div>

          <div className="input-row" style={{display:'flex', gap:'1.5rem'}}>
            <label>Turns
              <input type="number" value={turns} onChange={e=>setTurns(e.target.value)} style={{width:'80px'}}/>
            </label>
            <label>Simulations
              <input type="number" value={sims} onChange={e=>setSims(e.target.value)} style={{width:'80px'}}/>
            </label>
          </div>

          <button className="btn-primary" onClick={runBoardroom} disabled={loading}>
            {loading ? <><span className="spinner"></span> Orchestrating Debate...</> : 'Initiate Boardroom'}
          </button>
        </div>

        <div className="response-area">
          <h2>Debate Report</h2>
          <div 
            className="response-text" 
            dangerouslySetInnerHTML={{ __html: report || 'Awaiting boardroom initiation...' }} 
          />
        </div>
      </section>

      <aside className="sidebar">
        <div className="card">
          <h3>Engine Status</h3>
          <div className="status-list" style={{display:'flex', flexDirection:'column', gap:'1rem'}}>
            <div className="status-item" style={{display:'flex', justifyContent:'space-between'}}>
              <span className="text-secondary">Mode:</span>
              <span className="status-pill">Boardroom</span>
            </div>
            <div className="status-item" style={{display:'flex', justifyContent:'space-between'}}>
              <span className="text-secondary">Engine:</span>
              <span className="status-pill">Vertical AI</span>
            </div>
            <div className="status-item" style={{display:'flex', justifyContent:'space-between'}}>
              <span className="text-secondary">Status:</span>
              <span className={loading ? 'status-pill status-pill-active' : 'status-pill'}>
                {loading ? 'Running...' : 'Idle'}
              </span>
            </div>
          </div>
        </div>
      </aside>
    </div>
  )
}
