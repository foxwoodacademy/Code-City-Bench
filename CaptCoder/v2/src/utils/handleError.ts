import { useAppContext } from '../context/AppContext'

export function formatError(e:any) {
  if (!e) return { message: 'Unknown error', code: 'UNKNOWN' }
  if (e instanceof Error) return { message: e.message, code: (e as any).code || 'ERR' }
  if (typeof e === 'string') return { message: e, code: 'ERR_STRING' }
  return { message: JSON.stringify(e), code: 'ERR_JSON' }
}

export function useHandleError() {
  const { dispatch } = useAppContext()
  return (err:any, opts?: { userMessage?: string; code?: string; telemetry?: boolean }) => {
    const formatted = formatError(err)
    const entry = {
      timestamp: new Date().toISOString(),
      code: opts?.code ?? formatted.code,
      message: opts?.userMessage ?? formatted.message,
      details: formatted,
    }
    dispatch({ type: 'LOG_ERROR', payload: entry })
    return entry.message
  }
}
