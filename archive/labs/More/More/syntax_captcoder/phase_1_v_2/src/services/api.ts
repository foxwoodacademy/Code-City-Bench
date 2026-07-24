/**
 * services/api.ts
 * - Injects targeted context from contextManager into system instruction
 * - Default model selection set to gemini-2.5-flash (fast)
 * - Expects a backend proxy endpoint that will call the actual AI provider (do NOT put API keys in client)
 */

import { queryContext } from './contextManager'

export type Model = 'gemini-2.5-flash' | 'gemini-2.5-pro' | 'other'

const DEFAULT_MODEL: Model = 'gemini-2.5-flash'

export async function callAIWithContext(apiEndpoint: string, userMessage: string, opts?: { model?: Model, apiKey?: string }) {
  // 1) Query context manager for relevant snippets
  const { contextString, sources } = queryContext(userMessage, 1200)

  // 2) Build system instruction with provenance & brief
  const systemInstruction = [
    "You are the CaptCoder Guided Repair Assistant.",
    "Use only the context provided below to inform your guidance. Be concise, practical, and prioritize non-destructive steps.",
    "Provenance: " + (sources.length ? sources.join(', ') : 'none'),
    "",
    "Context:",
    contextString || "(no relevant context found)",
    "",
    "User message:",
    userMessage
  ].join('\n')

  // 3) Prepare payload for backend (backend should forward to the proper model/provider)
  const model = opts?.model ?? DEFAULT_MODEL
  const body = { model, systemInstruction, userMessage }

  try {
    const res = await fetch(apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type':'application/json',
        ...(opts?.apiKey ? { Authorization: `Bearer ${opts.apiKey}` } : {})
      },
      body: JSON.stringify(body)
    })
    if (!res.ok) {
      const txt = await res.text()
      throw new Error(`AI proxy error ${res.status}: ${txt}`)
    }
    const data = await res.json()
    // expect backend to return { ok:true, reply: string }
    if (!data || !data.reply) throw new Error('Malformed AI response')
    return { ok:true, reply: data.reply, sources }
  } catch (e:any) {
    return { ok:false, error: e.message || String(e) }
  }
}
