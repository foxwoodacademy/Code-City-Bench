// services/api.ts - lightweight wrapper (uses fetch). For demo, no external telemetry.
export async function callAI(endpoint:string, body:any, apiKey?:string) {
  try {
    const res = await fetch(endpoint, {
      method:'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(apiKey ? { Authorization: `Bearer ${apiKey}` } : {}),
      },
      body: JSON.stringify(body),
    })
    if (!res.ok) {
      const text = await res.text()
      return { ok:false, status: res.status, error: text }
    }
    const data = await res.json()
    return { ok:true, data }
  } catch(e){
    return { ok:false, status: 0, error: e.message || String(e) }
  }
}
