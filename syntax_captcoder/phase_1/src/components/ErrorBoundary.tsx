import React from 'react'
import { useAppContext } from '../context/AppContext'

class ErrorBoundaryInner extends React.Component<any, { hasError: boolean; error?: any }> {
  constructor(props:any){
    super(props)
    this.state = { hasError: false }
  }
  static getDerivedStateFromError(error:any) {
    return { hasError: true, error }
  }
  componentDidCatch(error:any, info:any) {
    if (this.props.onReport) this.props.onReport(error, info)
  }
  render(){
    if (this.state.hasError) {
      return (
        <div style={{padding:24, textAlign:'center'}}>
          <h2 style={{fontSize:20, fontWeight:700}}>Something went wrong.</h2>
          <p style={{marginTop:8}}>We captured the problem and will guide you to recover. Try reloading, or open Settings → Support.</p>
          <button style={{marginTop:12, padding:'8px 12px'}} onClick={()=>window.location.reload()}>Reload</button>
        </div>
      )
    }
    return this.props.children
  }
}

export const ErrorBoundary: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { dispatch } = useAppContext()
  return (
    <ErrorBoundaryInner
      onReport={(err:any, info:any) => {
        dispatch({
          type: 'LOG_ERROR',
          payload: { timestamp: new Date().toISOString(), code: 'RENDER_ERROR', message: err?.message || 'render error', details: info },
        })
      }}
    >
      {children}
    </ErrorBoundaryInner>
  )
}
