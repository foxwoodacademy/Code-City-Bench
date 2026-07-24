import { useState } from "react";

const API_URL = "https://api.anthropic.com/v1/messages";

const fibLabels = ["Tiny Fib", "White Lie", "Creative Truth", "Full Fiction", "Oscar-Worthy"];
const styleLabels = ["Apologetic", "Confident", "Dramatic", "Casual", "Elaborate"];
const relationshipOptions = ["Boss", "Partner", "Friend", "Parent", "Coworker", "Teacher", "Stranger"];

function Slider({ label, value, onChange, min = 1, max = 5, valueLabels }) {
  return (
    <div style={{ marginBottom: "1.4rem" }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.4rem" }}>
        <span style={{ color: "#aaa", fontSize: "0.78rem", letterSpacing: "0.12em", textTransform: "uppercase" }}>{label}</span>
        <span style={{ color: "#ff6b35", fontSize: "0.82rem", fontWeight: 700 }}>{valueLabels ? valueLabels[value - 1] : value}</span>
      </div>
      <input
        type="range" min={min} max={max} value={value}
        onChange={e => onChange(Number(e.target.value))}
        style={{ width: "100%", accentColor: "#ff6b35", cursor: "pointer", height: "4px" }}
      />
      {valueLabels && (
        <div style={{ display: "flex", justifyContent: "space-between", marginTop: "0.2rem" }}>
          {valueLabels.map((l, i) => (
            <span key={i} style={{ fontSize: "0.6rem", color: value === i + 1 ? "#ff6b35" : "#444", transition: "color 0.2s" }}>|</span>
          ))}
        </div>
      )}
    </div>
  );
}

export default function AskHole() {
  const [who, setWho] = useState("");
  const [event, setEvent] = useState("");
  const [relationship, setRelationship] = useState("Friend");
  const [importance, setImportance] = useState(3);
  const [fibLevel, setFibLevel] = useState(2);
  const [style, setStyle] = useState(2);
  const [detail, setDetail] = useState(3);
  const [excuse, setExcuse] = useState("");
  const [askholeScore, setAskholeScore] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  async function generateExcuse() {
    if (!who.trim() || !event.trim()) {
      setError("Fill in who and what first!");
      return;
    }
    setError("");
    setLoading(true);
    setExcuse("");
    setAskholeScore(null);

    const prompt = `You are AskHole — a darkly witty excuse-generation engine for people who need to get out of things.

Generate a believable excuse for this situation:
- Who it's for: ${who}
- The event/obligation: ${event}
- Relationship: ${relationship}
- Importance of the event (1=trivial, 5=critical): ${importance}
- Fib level (1=tiny white lie, 5=full fiction/oscar-worthy): ${fibLevel} (${fibLabels[fibLevel-1]})
- Excuse style (1=apologetic, 5=elaborate story): ${style} (${styleLabels[style-1]})
- Detail level (1=brief, 5=very detailed): ${detail}

Respond ONLY with valid JSON, no markdown, no backticks:
{
  "excuse": "the full excuse text ready to say or send",
  "askhole_score": <number 1-100 rating how much of an askhole this makes them>,
  "score_reason": "one witty sentence explaining the score"
}`;

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          messages: [{ role: "user", content: prompt }]
        })
      });
      const data = await res.json();
      const text = data.content?.map(b => b.text || "").join("") || "";
      const clean = text.replace(/```json|```/g, "").trim();
      const parsed = JSON.parse(clean);
      setExcuse(parsed.excuse);
      setAskholeScore({ score: parsed.askhole_score, reason: parsed.score_reason });
    } catch (e) {
      setError("Something went wrong. Try again.");
    }
    setLoading(false);
  }

  function copyExcuse() {
    navigator.clipboard.writeText(excuse);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  const scoreColor = askholeScore
    ? askholeScore.score < 30 ? "#4ade80"
    : askholeScore.score < 60 ? "#facc15"
    : askholeScore.score < 80 ? "#fb923c"
    : "#ef4444"
    : "#ff6b35";

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0a0a0a",
      fontFamily: "'Georgia', serif",
      color: "#e8e8e8",
      padding: "2rem 1rem",
      backgroundImage: "radial-gradient(ellipse at 20% 10%, #1a0800 0%, transparent 60%), radial-gradient(ellipse at 80% 90%, #0d0d1a 0%, transparent 60%)"
    }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Mono:wght@400;500&display=swap');
        input[type=range]::-webkit-slider-thumb { width: 16px; height: 16px; }
        ::placeholder { color: #444; }
        * { box-sizing: border-box; }
        .btn-main:hover { background: #e55a28 !important; transform: translateY(-1px); }
        .btn-main:active { transform: translateY(0); }
        .copy-btn:hover { background: #1a1a1a !important; }
      `}</style>

      <div style={{ maxWidth: "560px", margin: "0 auto" }}>

        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
          <div style={{ fontSize: "0.72rem", letterSpacing: "0.3em", color: "#ff6b35", textTransform: "uppercase", marginBottom: "0.6rem", fontFamily: "'DM Mono', monospace" }}>
            ◆ Excuse Engine v1.0 ◆
          </div>
          <h1 style={{
            fontFamily: "'Playfair Display', serif",
            fontSize: "clamp(3rem, 12vw, 5rem)",
            fontWeight: 900,
            margin: 0,
            lineHeight: 1,
            background: "linear-gradient(135deg, #ff6b35, #ff9a5c, #ffbd80)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent"
          }}>AskHole</h1>
          <p style={{ color: "#555", fontSize: "0.85rem", marginTop: "0.5rem", fontFamily: "'DM Mono', monospace", letterSpacing: "0.05em" }}>
            Believable excuses for people who need them
          </p>
        </div>

        {/* Form Card */}
        <div style={{
          background: "#111",
          border: "1px solid #222",
          borderRadius: "12px",
          padding: "1.8rem",
          marginBottom: "1.2rem"
        }}>
          <div style={{ marginBottom: "1.2rem" }}>
            <label style={{ display: "block", fontSize: "0.72rem", letterSpacing: "0.15em", color: "#666", textTransform: "uppercase", marginBottom: "0.5rem", fontFamily: "'DM Mono', monospace" }}>
              Who is the excuse for?
            </label>
            <input
              value={who}
              onChange={e => setWho(e.target.value)}
              placeholder="e.g. My boss, Sarah, Mom..."
              style={{
                width: "100%", background: "#0d0d0d", border: "1px solid #2a2a2a",
                borderRadius: "8px", padding: "0.7rem 1rem", color: "#e8e8e8",
                fontSize: "0.95rem", outline: "none", fontFamily: "inherit"
              }}
            />
          </div>

          <div style={{ marginBottom: "1.5rem" }}>
            <label style={{ display: "block", fontSize: "0.72rem", letterSpacing: "0.15em", color: "#666", textTransform: "uppercase", marginBottom: "0.5rem", fontFamily: "'DM Mono', monospace" }}>
              What are you getting out of?
            </label>
            <input
              value={event}
              onChange={e => setEvent(e.target.value)}
              placeholder="e.g. Monday morning meeting, dinner party..."
              style={{
                width: "100%", background: "#0d0d0d", border: "1px solid #2a2a2a",
                borderRadius: "8px", padding: "0.7rem 1rem", color: "#e8e8e8",
                fontSize: "0.95rem", outline: "none", fontFamily: "inherit"
              }}
            />
          </div>

          <div style={{ marginBottom: "1.5rem" }}>
            <label style={{ display: "block", fontSize: "0.72rem", letterSpacing: "0.15em", color: "#666", textTransform: "uppercase", marginBottom: "0.6rem", fontFamily: "'DM Mono', monospace" }}>
              Relationship
            </label>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
              {relationshipOptions.map(r => (
                <button key={r} onClick={() => setRelationship(r)} style={{
                  padding: "0.35rem 0.9rem", borderRadius: "20px", fontSize: "0.82rem",
                  border: relationship === r ? "1px solid #ff6b35" : "1px solid #2a2a2a",
                  background: relationship === r ? "#1a0800" : "#0d0d0d",
                  color: relationship === r ? "#ff6b35" : "#666",
                  cursor: "pointer", transition: "all 0.15s", fontFamily: "'DM Mono', monospace"
                }}>{r}</button>
              ))}
            </div>
          </div>

          <div style={{ borderTop: "1px solid #1a1a1a", paddingTop: "1.4rem" }}>
            <Slider label="Fib Level" value={fibLevel} onChange={setFibLevel} valueLabels={fibLabels} />
            <Slider label="Excuse Style" value={style} onChange={setStyle} valueLabels={styleLabels} />
            <Slider label="Event Importance" value={importance} onChange={setImportance} valueLabels={["Trivial","Minor","Moderate","Important","Critical"]} />
            <Slider label="Detail Level" value={detail} onChange={setDetail} valueLabels={["Brief","Light","Medium","Detailed","Elaborate"]} />
          </div>

          {error && <p style={{ color: "#ef4444", fontSize: "0.82rem", marginBottom: "1rem", fontFamily: "'DM Mono', monospace" }}>{error}</p>}

          <button
            className="btn-main"
            onClick={generateExcuse}
            disabled={loading}
            style={{
              width: "100%", padding: "0.9rem", background: "#ff6b35",
              color: "#fff", border: "none", borderRadius: "8px",
              fontSize: "0.9rem", fontWeight: 700, cursor: loading ? "not-allowed" : "pointer",
              letterSpacing: "0.1em", textTransform: "uppercase",
              fontFamily: "'DM Mono', monospace", transition: "all 0.15s",
              opacity: loading ? 0.7 : 1
            }}
          >
            {loading ? "Crafting your escape..." : "Generate Excuse"}
          </button>
        </div>

        {/* Result */}
        {excuse && (
          <div style={{
            background: "#111", border: "1px solid #222", borderRadius: "12px",
            padding: "1.8rem", animation: "fadeIn 0.4s ease"
          }}>
            <style>{`@keyframes fadeIn { from { opacity:0; transform:translateY(8px) } to { opacity:1; transform:translateY(0) } }`}</style>

            <div style={{ fontSize: "0.72rem", letterSpacing: "0.15em", color: "#ff6b35", textTransform: "uppercase", marginBottom: "0.8rem", fontFamily: "'DM Mono', monospace" }}>
              Your Excuse
            </div>

            <p style={{ fontSize: "1rem", lineHeight: 1.7, color: "#ddd", marginBottom: "1.2rem", borderLeft: "2px solid #ff6b35", paddingLeft: "1rem" }}>
              {excuse}
            </p>

            <button className="copy-btn" onClick={copyExcuse} style={{
              background: "#0d0d0d", border: "1px solid #2a2a2a", color: copied ? "#4ade80" : "#888",
              padding: "0.45rem 1rem", borderRadius: "6px", cursor: "pointer",
              fontSize: "0.78rem", fontFamily: "'DM Mono', monospace", transition: "all 0.15s",
              marginBottom: "1.2rem"
            }}>
              {copied ? "✓ Copied!" : "Copy to clipboard"}
            </button>

            {askholeScore && (
              <div style={{ background: "#0d0d0d", borderRadius: "8px", padding: "1rem", border: "1px solid #1a1a1a" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "0.8rem", marginBottom: "0.4rem" }}>
                  <span style={{ fontSize: "0.72rem", letterSpacing: "0.15em", color: "#555", textTransform: "uppercase", fontFamily: "'DM Mono', monospace" }}>AskHole Score</span>
                  <span style={{ fontSize: "1.4rem", fontWeight: 900, color: scoreColor, fontFamily: "'Playfair Display', serif" }}>{askholeScore.score}</span>
                  <span style={{ fontSize: "0.72rem", color: "#444", fontFamily: "'DM Mono', monospace" }}>/100</span>
                </div>
                <p style={{ fontSize: "0.82rem", color: "#666", margin: 0, fontStyle: "italic" }}>{askholeScore.reason}</p>
              </div>
            )}
          </div>
        )}

        <p style={{ textAlign: "center", color: "#2a2a2a", fontSize: "0.7rem", marginTop: "2rem", fontFamily: "'DM Mono', monospace" }}>
          AskHole — Use responsibly. Or don't.
        </p>
      </div>
    </div>
  );
}
