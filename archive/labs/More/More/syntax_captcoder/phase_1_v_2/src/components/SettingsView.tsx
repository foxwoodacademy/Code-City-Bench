import React, { useState } from 'react'
import { useAppContext } from '../context/AppContext'

export const SettingsView: React.FC = () => {
  const { state, dispatch } = useAppContext()
  const [open, setOpen] = useState<{ [k:string]: boolean }>({ general: true, privacy: false, developer: false })

  return (
    <div>
      <h2 style={{fontSize:18,fontWeight:700}}>Settings</h2>
      <p style={{marginTop:6, fontSize:13, color:'#555'}}>This panel is intentionally verbose. It contains controls for both novice and advanced users.</p>

      <div style={{marginTop:12}}>
        <label style={{display:'flex',alignItems:'center',gap:10}}>
          <input type="checkbox" checked={state.simpleMode} onChange={()=>dispatch({ type: 'TOGGLE_SIMPLE_MODE' })} />
          <span>Simple Mode (hide advanced stuff)</span>
        </label>
      </div>

      <div style={{marginTop:14,border:'1px solid #eee', borderRadius:8}}>
        <button style={{width:'100%', textAlign:'left', padding:12}} onClick={()=>setOpen(s=>({...s, general: !s.general}))}>
          <div style={{display:'flex',justifyContent:'space-between', alignItems:'center'}}>
            <span style={{fontWeight:600}}>General</span>
            <span>{open.general ? '−' : '+'}</span>
          </div>
        </button>
        {open.general && (
          <div style={{padding:12, borderTop:'1px solid #f5f5f5'}}>
            <label>
              API Key
              <input className="input" style={{marginTop:8}} value={state.apiKey ?? ''} onChange={(e)=>dispatch({ type: 'SET_API_KEY', payload: e.target.value })} placeholder="Paste your API key (kept local only)" />
            </label>
            <div style={{marginTop:8,fontSize:12,color:'#666'}}>Your API key is stored locally in your browser. It is not uploaded unless you explicitly enable telemetry.</div>
          </div>
        )}
      </div>

      <div style={{marginTop:12,border:'1px solid #eee', borderRadius:8}}>
        <button style={{width:'100%', textAlign:'left', padding:12}} onClick={()=>setOpen(s=>({...s, privacy: !s.privacy}))}>
          <div style={{display:'flex',justifyContent:'space-between', alignItems:'center'}}>
            <span style={{fontWeight:600}}>Privacy & Data</span>
            <span>{open.privacy ? '−' : '+'}</span>
          </div>
        </button>
        {open.privacy && (
          <div style={{padding:12, borderTop:'1px solid #f5f5f5', fontSize:13}}>
            <p><strong>What we do:</strong> The app processes images and audio temporarily to generate guidance. By default, no raw media is stored on remote servers.</p>
            <p style={{marginTop:8}}><strong>API Keys:</strong> Your API key is kept locally in your browser storage. It is used by the app to call the AI service you choose and is not sent to any third-party analytics service by default.</p>
            <p style={{marginTop:8}}><strong>Telemetry:</strong> Optional, opt-in only. Telemetry collects anonymized events (permission denials, fatal crashes) to help us fix reliability issues. No user content is sent without your explicit approval.</p>
            <div style={{marginTop:8}}>
              <label style={{display:'flex', gap:8, alignItems:'center'}}>
                <input type="checkbox" /> <span>Enable optional telemetry (helps improve app)</span>
              </label>
            </div>
          </div>
        )}
      </div>

      {!state.simpleMode && (
        <div style={{marginTop:12,border:'1px solid #eee', borderRadius:8}}>
          <button style={{width:'100%', textAlign:'left', padding:12}} onClick={()=>setOpen(s=>({...s, developer: !s.developer}))}>
            <div style={{display:'flex',justifyContent:'space-between', alignItems:'center'}}>
              <span style={{fontWeight:600}}>Developer (Verbose)</span>
              <span>{open.developer ? '−' : '+'}</span>
            </div>
          </button>
          {open.developer && (
            <div style={{padding:12,borderTop:'1px solid #f5f5f5', fontSize:13}}>
              <p style={{marginBottom:8}}>Control debug & dev-level behaviors.</p>
              <label>
                <span style={{fontSize:12,color:'#666'}}>Context injection level</span>
                <select className="input" defaultValue="minimal" style={{marginTop:8}}>
                  <option value="minimal">Minimal (short snippets)</option>
                  <option value="balanced">Balanced (tiered RAG)</option>
                  <option value="full">Full (developer only — expensive)</option>
                </select>
              </label>

              <div style={{marginTop:12}}>
                <button className="btn-outline" onClick={()=>localStorage.clear()}>Clear Local Storage</button>
                <button className="btn" style={{marginLeft:8}} onClick={()=>dispatch({ type: 'CLEAR_CONVERSATION' })}>Clear Conversation</button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
