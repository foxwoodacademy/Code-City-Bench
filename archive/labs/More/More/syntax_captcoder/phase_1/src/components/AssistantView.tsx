import React, { useState } from 'react'
import { useAppContext } from '../context/AppContext'

export const AssistantView: React.FC = () => {
  const { state, dispatch } = useAppContext()
  const [text, setText] = useState('')

  const send = () => {
    if (!text.trim()) return
    dispatch({ type: 'ADD_MESSAGE', payload: { role: 'user', text } })
    // placeholder: push assistant reply
    dispatch({ type: 'ADD_MESSAGE', payload: { role: 'assistant', text: 'Processing... (connect your AI backend)' } })
    setText('')
  }

  return (
    <div>
      <h1 style={{fontSize:20,fontWeight:700}}>Guided Repair Assistant</h1>
      <div style={{marginTop:12}}>
        <div style={{border:'1px solid #eee', borderRadius:8, padding:12, minHeight:220}}>
          {state.conversation.length === 0 ? <div style={{color:'#666'}}>Say something or paste a problem description to begin.</div> : null}
          {state.conversation.map((m, i) => (
            <div key={i} style={{marginBottom:8}}>
              <div style={{fontSize:12, color:'#666'}}>{m.role}</div>
              <div style={{padding:8, background:m.role==='user' ? '#f9fafb' : '#eef2ff', borderRadius:6}}>{m.text}</div>
            </div>
          ))}
        </div>

        <div style={{display:'flex', gap:8, marginTop:12}}>
          <input className="input" value={text} onChange={(e)=>setText(e.target.value)} placeholder="Describe the issue (e.g., 'screen dead, phone powers on')" />
          <button className="btn" onClick={send}>Send</button>
        </div>
      </div>
    </div>
  )
}
