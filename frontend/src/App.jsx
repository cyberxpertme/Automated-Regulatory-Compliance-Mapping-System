import { useState, useEffect } from "react"
import axios from "axios"
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts"

const API = "http://localhost:8001"
const COLORS = ["#22c55e", "#f59e0b"]

export default function App() {
  const [stats, setStats] = useState(null)
  const [mappings, setMappings] = useState([])
  const [nlpResult, setNlpResult] = useState(null)
  const [activeTab, setActiveTab] = useState("dashboard")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    axios.get(`${API}/mapping/stats`)
      .then(r => { console.log("stats:", r.data); setStats(r.data) })
      .catch(e => { console.log("stats error:", e); setError("Backend connect failed!") })

    axios.get(`${API}/mapping/sample`)
      .then(r => { console.log("mappings:", r.data); setMappings(r.data.mappings) })
      .catch(e => console.log("mappings error:", e))
  }, [])

  const runNlpDemo = async () => {
    setLoading(true)
    try {
      const res = await axios.get(`${API}/nlp/demo`)
      setNlpResult(res.data)
    } catch(e) {
      setError("NLP failed: " + e.message)
    }
    setLoading(false)
  }

  const pieData = stats ? [
    { name: "Full Coverage", value: stats.full_coverage },
    { name: "Partial Coverage", value: stats.partial_coverage },
  ] : []

  const barData = mappings.map(m => ({
    name: m.source_control_id,
    confidence: Math.round(m.confidence_score * 100),
  }))

  return (
    <div style={{ fontFamily: "sans-serif", background: "#0f172a", minHeight: "100vh", color: "white" }}>
      <div style={{ background: "#1e293b", padding: "20px 40px", borderBottom: "1px solid #334155" }}>
        <h1 style={{ margin: 0, color: "#38bdf8", fontSize: "1.3rem" }}>🛡️ Automated Regulatory Compliance Mapping System</h1>
        <p style={{ margin: "4px 0 0", color: "#94a3b8", fontSize: "0.85rem" }}>University of Dhaka — PMICS Batch 4 | H-411 & H-392</p>
      </div>

      {error && (
        <div style={{ background: "#7f1d1d", color: "#fca5a5", padding: "10px 40px", fontSize: "0.85rem" }}>
          ⚠️ {error}
        </div>
      )}

      <div style={{ display: "flex", gap: "8px", padding: "20px 40px 0" }}>
        {[{ id: "dashboard", label: "📊 Dashboard" }, { id: "mappings", label: "🗺️ Mappings" }, { id: "nlp", label: "🧠 NLP Engine" }].map(tab => (
          <button key={tab.id} onClick={() => setActiveTab(tab.id)}
            style={{ padding: "8px 20px", borderRadius: "8px", border: "none", cursor: "pointer", fontWeight: "bold",
              background: activeTab === tab.id ? "#38bdf8" : "#1e293b",
              color: activeTab === tab.id ? "#0f172a" : "#94a3b8" }}>
            {tab.label}
          </button>
        ))}
      </div>

      <div style={{ padding: "30px 40px" }}>

        {activeTab === "dashboard" && (
          <div>
            {!stats ? (
              <div style={{ color: "#94a3b8", fontSize: "1rem" }}>
                ⏳ Loading stats from backend...
                <br/><br/>
                <span style={{ fontSize: "0.8rem" }}>Backend: {API}</span>
              </div>
            ) : (
              <>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "16px", marginBottom: "30px" }}>
                  {[
                    { label: "Total Controls", value: stats.total_controls, color: "#38bdf8" },
                    { label: "Full Coverage", value: stats.full_coverage, color: "#22c55e" },
                    { label: "Partial Coverage", value: stats.partial_coverage, color: "#f59e0b" },
                    { label: "Avg Confidence", value: `${stats.average_confidence}%`, color: "#a78bfa" },
                  ].map(card => (
                    <div key={card.label} style={{ background: "#1e293b", borderRadius: "12px", padding: "20px", borderTop: `3px solid ${card.color}` }}>
                      <div style={{ fontSize: "2rem", fontWeight: "bold", color: card.color }}>{card.value}</div>
                      <div style={{ color: "#94a3b8", fontSize: "0.85rem", marginTop: "4px" }}>{card.label}</div>
                    </div>
                  ))}
                </div>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
                  <div style={{ background: "#1e293b", borderRadius: "12px", padding: "20px" }}>
                    <h3 style={{ margin: "0 0 16px", color: "#e2e8f0" }}>Coverage Breakdown</h3>
                    <ResponsiveContainer width="100%" height={220}>
                      <PieChart>
                        <Pie data={pieData} cx="50%" cy="50%" outerRadius={80} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                          {pieData.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                  <div style={{ background: "#1e293b", borderRadius: "12px", padding: "20px" }}>
                    <h3 style={{ margin: "0 0 16px", color: "#e2e8f0" }}>Confidence by Control</h3>
                    <ResponsiveContainer width="100%" height={220}>
                      <BarChart data={barData}>
                        <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 11 }} />
                        <YAxis tick={{ fill: "#94a3b8" }} domain={[0, 100]} unit="%" />
                        <Tooltip formatter={(v) => `${v}%`} />
                        <Bar dataKey="confidence" fill="#38bdf8" radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </>
            )}
          </div>
        )}

        {activeTab === "mappings" && (
          <div style={{ background: "#1e293b", borderRadius: "12px", overflow: "hidden" }}>
            {mappings.length === 0 ? (
              <div style={{ padding: "20px", color: "#94a3b8" }}>⏳ Loading mappings...</div>
            ) : (
              <table style={{ width: "100%", borderCollapse: "collapse" }}>
                <thead>
                  <tr style={{ background: "#0f172a" }}>
                    {["ISO 27001", "Title", "NIST CSF", "Confidence", "Gap"].map(h => (
                      <th key={h} style={{ padding: "12px 16px", textAlign: "left", color: "#38bdf8", fontSize: "0.85rem" }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {mappings.map((m, i) => (
                    <tr key={i} style={{ borderTop: "1px solid #334155" }}>
                      <td style={{ padding: "12px 16px", color: "#38bdf8", fontWeight: "bold" }}>{m.source_control_id}</td>
                      <td style={{ padding: "12px 16px", color: "#e2e8f0", fontSize: "0.85rem" }}>{m.source_control_title}</td>
                      <td style={{ padding: "12px 16px", color: "#a78bfa" }}>{m.target_control_id}</td>
                      <td style={{ padding: "12px 16px" }}>
                        <span style={{ background: m.confidence_score > 0.85 ? "#14532d" : "#713f12",
                          color: m.confidence_score > 0.85 ? "#22c55e" : "#f59e0b",
                          padding: "2px 10px", borderRadius: "20px", fontSize: "0.8rem" }}>
                          {Math.round(m.confidence_score * 100)}%
                        </span>
                      </td>
                      <td style={{ padding: "12px 16px", color: "#94a3b8", fontSize: "0.8rem" }}>
                        {m.gap_description || "✅ Full Match"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}

        {activeTab === "nlp" && (
          <div>
            <div style={{ background: "#1e293b", borderRadius: "12px", padding: "24px", marginBottom: "20px" }}>
              <h3 style={{ margin: "0 0 12px", color: "#e2e8f0" }}>🧠 NLP Clause Extraction Demo</h3>
              <p style={{ color: "#94a3b8", marginBottom: "16px" }}>Click to run NLP extraction on sample ISO 27001 text using spaCy.</p>
              <button onClick={runNlpDemo} disabled={loading}
                style={{ background: "#38bdf8", color: "#0f172a", padding: "10px 24px",
                  borderRadius: "8px", border: "none", cursor: "pointer", fontWeight: "bold" }}>
                {loading ? "Processing..." : "▶ Run NLP Demo"}
              </button>
            </div>
            {nlpResult && (
              <div>
                <div style={{ color: "#22c55e", marginBottom: "16px" }}>
                  ✅ Found <strong>{nlpResult.total_clauses_found}</strong> compliance clauses
                </div>
                {nlpResult.clauses.map((c, i) => (
                  <div key={i} style={{ background: "#1e293b", borderRadius: "8px", padding: "16px",
                    marginBottom: "10px", borderLeft: "3px solid #38bdf8" }}>
                    <div style={{ color: "#38bdf8", fontSize: "0.8rem", marginBottom: "6px" }}>
                      {c.clause_id} | Confidence: {Math.round(c.confidence * 100)}%
                    </div>
                    <div style={{ color: "#e2e8f0", fontSize: "0.9rem" }}>{c.text}</div>
                    <div style={{ color: "#64748b", fontSize: "0.75rem", marginTop: "6px" }}>
                      Keywords: {c.matched_keywords.join(", ")}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
