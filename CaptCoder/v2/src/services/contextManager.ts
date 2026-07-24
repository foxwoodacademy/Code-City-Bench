import contextJSON from '../data/context.json';
import type { ConversationContext } from '../types';

/**
 * Lightweight keyword-based RAG: selects relevant snippets from context.json
 * based on simple token scoring. Meant as Phase1 RAG to avoid stuffing full JSON.
 */

type Snippet = { path: string; text: string; score?: number };

function extractSnippets(ctx: any, prefix = ''): Snippet[] {
  const out: Snippet[] = [];
  if (typeof ctx === 'string' || typeof ctx === 'number' || typeof ctx === 'boolean') {
    out.push({ path: prefix, text: String(ctx) });
    return out;
  }
  if (Array.isArray(ctx)) {
    ctx.forEach((v, i) => out.push(...extractSnippets(v, `${prefix}[${i}]`)));
    return out;
  }
  Object.keys(ctx).forEach(k => {
    const v = ctx[k];
    const path = prefix ? `${prefix}.${k}` : k;
    if (typeof v === 'string' && v.length < 1200) out.push({ path, text: v });
    else if (typeof v === 'object') out.push(...extractSnippets(v, path));
  });
  return out;
}

const SNIPPETS: Snippet[] = extractSnippets(contextJSON);

/**
 * Score a snippet by keyword hits (case-insensitive).
 */
function scoreSnippet(snippet: Snippet, tokens: string[]) {
  const low = snippet.text.toLowerCase();
  let score = 0;
  tokens.forEach(t => {
    if (!t) return;
    const re = new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
    const m = low.match(re);
    if (m) score += m.length;
  });
  return score;
}

/**
 * Query the context manager with a user query. Returns a trimmed context string
 * containing the highest scoring snippets concatenated together (with provenance).
 */
export function queryContext(query: string, maxTokens = 800): { contextString: string; sources: string[] } {
  const tokens = query.toLowerCase().split(/\W+/).filter(Boolean).slice(0, 30);
  const scored = SNIPPETS.map(s => ({ ...s, score: scoreSnippet(s, tokens) }));
  scored.sort((a, b) => (b.score || 0) - (a.score || 0));
  const selected: Snippet[] = [];
  const sources: string[] = [];
  let length = 0;
  for (const s of scored) {
    if (!s.score || s.score <= 0) break;
    const addLen = s.text.length;
    if (length + addLen > maxTokens) continue;
    selected.push(s);
    sources.push(s.path);
    length += addLen;
    if (selected.length >= 10) break;
  }
  const contextString = selected.map(s => `[${s.path}] ${s.text}`).join('\n---\n');
  return { contextString, sources };
}

/**
 * Utility: returns raw context JSON (typed) if needed elsewhere.
 */
export function getRawContext(): ConversationContext {
  return contextJSON as ConversationContext;
}
