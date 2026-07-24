import React, { useEffect, useState } from 'react'
import { useAppContext } from '../context/AppContext'

const checkPermission = async (name: 'camera'|'microphone') => {
  try {
    // @ts-ignore
    if (navigator.permissions && navigator.permissions.query) {
      // @ts-ignore
      const status = await navigator.permissions.query({ name })
      return status.state as 'granted'|'denied'|'prompt'
    }
  } catch(e){}
  return undefined
}

export const PermissionsGate: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { state, dispatch } = useAppContext()
  const [checked, setChecked] = useState(false)

  useEffect(() => {
    (async () => {
      const cam = await checkPermission('camera')
      const mic = await checkPermission('microphone')
      dispatch({ type: 'SET_PERMISSIONS', payload: { camera: cam, microphone: mic } })
      setChecked(true)
    })()
  }, [dispatch])

  const cameraOk = state.permissions.camera === 'granted' || state.simpleMode
  const micOk = state.permissions.microphone === 'granted' || state.simpleMode

  if (!checked) return <div style={{padding:20}}>Checking device permissions…</div>
  if (cameraOk && micOk) return <>{children}</>

  return (
    <div style={{padding:20, maxWidth:720, margin:'0 auto'}}>
      <h2 style={{fontSize:20,fontWeight:700}}>Permissions required</h2>
      <p style={{marginTop:8}}>
        To use voice and camera features, we need camera and microphone permissions. If you prefer not to grant them,
        switch the app to <strong>Simple Mode</strong> in Settings.
      </p>

      <div style={{marginTop:16, display:'grid', gap:12}}>
        {state.permissions.camera !== 'granted' && (
          <div style={{padding:12, border:'1px solid #eee', borderRadius:8}}>
            <h3 style={{fontWeight:600}}>Camera</h3>
            <p style={{fontSize:13}}>Needed to analyze hardware visually and to capture images.</p>
            <ol style={{marginLeft:18, fontSize:13}}>
              <li>Click "Enable Camera" below and allow access in your browser prompt.</li>
              <li>If denied, open your browser settings or system privacy settings and allow camera access for this site.</li>
            </ol>
            <div style={{marginTop:8}}>
              <button onClick={async ()=>{
                try {
                  await navigator.mediaDevices.getUserMedia({ video: true })
                  const cam = await (navigator.permissions?.query ? navigator.permissions.query({ name: 'camera' }) : Promise.resolve({ state: 'granted' }))
                  dispatch({ type: 'SET_PERMISSIONS', payload: { ...state.permissions, camera: (cam as any).state || 'granted' } })
                } catch(e){
                  dispatch({ type: 'LOG_ERROR', payload: { timestamp: new Date().toISOString(), code: 'CAM_DENY', message: 'Camera denied by user', details: e } })
                }
              }} className="btn">Enable Camera</button>
            </div>
          </div>
        )}

        {state.permissions.microphone !== 'granted' && (
          <div style={{padding:12, border:'1px solid #eee', borderRadius:8}}>
            <h3 style={{fontWeight:600}}>Microphone</h3>
            <p style={{fontSize:13}}>Needed for voice commands and hands-free operation.</p>
            <ol style={{marginLeft:18, fontSize:13}}>
              <li>Click "Enable Microphone" below and allow access in your browser prompt.</li>
              <li>If denied, open browser/system settings to re-enable.</li>
            </ol>
            <div style={{marginTop:8}}>
              <button onClick={async ()=>{
                try {
                  await navigator.mediaDevices.getUserMedia({ audio: true })
                  const mic = await (navigator.permissions?.query ? navigator.permissions.query({ name: 'microphone' }) : Promise.resolve({ state: 'granted' }))
                  dispatch({ type: 'SET_PERMISSIONS', payload: { ...state.permissions, microphone: (mic as any).state || 'granted' } })
                } catch(e){
                  dispatch({ type: 'LOG_ERROR', payload: { timestamp: new Date().toISOString(), code: 'MIC_DENY', message: 'Microphone denied by user', details: e } })
                }
              }} className="btn">Enable Microphone</button>
            </div>
          </div>
        )}
      </div>

      <div style={{marginTop:16, display:'flex', gap:8}}>
        <button onClick={()=>dispatch({ type: 'TOGGLE_SIMPLE_MODE', payload: true })} className="btn-outline">Switch to Simple Mode (No camera/mic)</button>
        <button onClick={()=>window.location.reload()} className="btn">Try Again</button>
      </div>

      <div style={{marginTop:12, fontSize:12, color:'#666'}}>If you need step-by-step help to change your browser permissions, open Settings → Support.</div>
    </div>
  )
}
