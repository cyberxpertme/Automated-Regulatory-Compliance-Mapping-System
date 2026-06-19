import { useState, useEffect } from "react"
import axios from "axios"
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts"

const API = "http://localhost:8001"
const COLORS = ["#22c55e", "#f59e0b"]

export default function App() {
  const [framework, setFramework] = useState("iso27001")
  const [stats, setStats] = useState(null)
  const [mappings, setMappings] = useState([])
  const [nlpResult, setNlpResult] = useState(null)
  const [activeTab, setActiveTab] = useState("dashboard")
  const [loading, setLoading] = useState(false)
  const [downloading, setDownloading] = useState(false)

  // Upload tab states
  const [uploadFile, setUploadFile] = useState(null)
  const [uploadResult, setUploadResult] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState(null)

  useEffect(() => {
    axios.get(`${API}/frameworks/${framework}/stats`).then(r => setStats(r.data)).catch(console.log)
    axios.get(`${API}/frameworks/${framework}/mappings`).then(r => setMappings(r.data.mappings)).catch(console.log)
  }, [framework])

  const runNlpDemo = async () => {
    setLoading(true)
    const res = await axios.get(`${API}/nlp/demo`)
    setNlpResult(res.data)
    setLoading(false)
  }

  const downloadReport = async () => {
    setDownloading(true)
    try {
      const response = await axios.get(`${API}/reports/download`, { responseType: "blob" })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement("a")
      link.href = url
      link.setAttribute("download", `compliance_report_${Date.now()}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (err) {
      alert("Download failed: " + err.message)
    }
    setDownloading(false)
  }

  const handleFileChange = (e) => {
    setUploadFile(e.target.files[0])
    setUploadResult(null)
    setUploadError(null)
  }

  const handleUpload = async () => {
    if (!uploadFile) return
    setUploading(true)
    setUploadError(null)
    const formData = new FormData()
    formData.append("file", uploadFile)
    try {
      const res = await axios.post(`${API}/upload/analyze`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      })
      setUploadResult(res.data)
    } catch (err) {
      setUploadError(err.response?.data?.detail || "Upload failed")
    }
    setUploading(false)
  }

  const pieData = stats ? [
    { name: "Full Coverage", value: stats.full_coverage },
    { name: "Partial Coverage", value: stats.partial_coverage },
  ] : []

  const barData = mappings.map(m => ({
    name: m.source_control_id,
    confidence: Math.round(m.confidence_score * 100),
  }))

  const frameworkNames = { iso27001: "ISO 27001:2022", pci_dss: "PCI-DSS v4.0" }

  return (
    <div style={{ fontFamily: "sans-serif", background: "#0f172a", minHeight: "100vh", color: "white" }}>
      <div style={{ background: "#1e293b", padding: "20px 40px", borderBottom: "1px solid #334155", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1 style={{ margin: 0, color: "#38bdf8", fontSize: "1.3rem" }}>🛡️ Automated Regulatory Compliance Mapping System</h1>
          <p style={{ margin: "4px 0 0", color: "#94a3b8", fontSize: "0.85rem" }}>University of Dhaka — PMICS Batch 4 | H-411 & H-392</p>
        </div>
        <button onClick={downloadReport} disabled={downloading}
          style={{ background: "#22c55e", color: "#0f172a", padding: "10px 20px", borderRadius: "8px", border: "none", cursor: "pointer", fontWeight: "bold", fontSize: "0.9rem" }}>
          {downloading ? "⏳ Generating..." : "📄 Download PDF Report"}
        </button>
      </div>

      <div style={{ display: "flex", justifyContent: "space-between", padding: "20px 40px 0", alignItems: "center", flexWrap: "wrap", gap: "10px" }}>
        <div style={{ display: "flex", gap: "8px" }}>
          {[
            { id: "dashboard", label: "📊 Dashboard" },
            { id: "mappings", label: "🗺️ Mappings" },
            { id: "nlp", label: "🧠 NLP Engine" },
            { id: "upload", label: "📤 Upload & Auto-Map" },
          ].map(tab => (
            <button key={tab.id} onClick={() => setActiveTab(tab.id)}
              style={{ padding: "8px 18px", borderRadius: "8px", border: "none", cursor: "pointer", fontWeight: "bold", fontSize: "0.85rem",
                background: activeTab === tab.id ? "#38bdf8" : "#1e293b", color: activeTab === tab.id ? "#0f172a" : "#94a3b8" }}>
              {tab.label}
            </button>
          ))}
        </div>

        {activeTab !== "upload" && (
          <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
            <span style={{ color: "#94a3b8", fontSize: "0.85rem" }}>Framework:</span>
            {Object.keys(frameworkNames).map(fw => (
              <button key={fw} onClick={() => setFramework(fw)}
                style={{ padding: "6px 16px", borderRadius: "20px", border: framework === fw ? "1px solid #a78bfa" : "1px solid #334155",
                  cursor: "pointer", fontSize: "0.8rem", fontWeight: "bold",
                  background: framework === fw ? "#a78bfa" : "#1e293b", color: framework === fw ? "#0f172a" : "#94a3b8" }}>
                {frameworkNames[fw]}
              </button>
            ))}
          </div>
        )}
      </div>

      <div style={{ padding: "30px 40px" }}>

        {activeTab === "dashboard" && stats && (
          <div>
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
                    <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 9 }} />
                    <YAxis tick={{ fill: "#94a3b8" }} domain={[0, 100]} unit="%" />
                    <Tooltip formatter={(v) => `${v}%`} />
                    <Bar dataKey="confidence" fill="#38bdf8" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {activeTab === "mappings" && (
          <div style={{ background: "#1e293b", borderRadius: "12px", overflow: "hidden", overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ background: "#0f172a" }}>
                  {[frameworkNames[framework], "Title", "NIST CSF", "Confidence", "Gap"].map(h => (
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
                        color: m.confidence_score > 0.85 ? "#22c55e" : "#f59e0b", padding: "2px 10px", borderRadius: "20px", fontSize: "0.8rem" }}>
                        {Math.round(m.confidence_score * 100)}%
                      </span>
                    </td>
                    <td style={{ padding: "12px 16px", color: "#94a3b8", fontSize: "0.8rem" }}>{m.gap_description || "✅ Full Match"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === "nlp" && (
          <div>
            <div style={{ background: "#1e293b", borderRadius: "12px", padding: "24px", marginBottom: "20px" }}>
              <h3 style={{ margin: "0 0 12px", color: "#e2e8f0" }}>🧠 NLP Clause Extraction Demo</h3>
              <p style={{ color: "#94a3b8", marginBottom: "16px" }}>Click to run NLP extraction with TF-IDF similarity scoring.</p>
              <button onClick={runNlpDemo} disabled={loading}
                style={{ background: "#38bdf8", color: "#0f172a", padding: "10px 24px", borderRadius: "8px", border: "none", cursor: "pointer", fontWeight: "bold" }}>
                {loading ? "Processing..." : "▶ Run NLP Demo"}
              </button>
            </div>
            {nlpResult && (
              <div>
                <div style={{ color: "#22c55e", marginBottom: "16px" }}>
                  ✅ Found <strong>{nlpResult.total_clauses_found}</strong> clauses | Avg Confidence: <strong>{nlpResult.average_confidence}%</strong>
                </div>
                {nlpResult.clauses.map((c, i) => (
                  <div key={i} style={{ background: "#1e293b", borderRadius: "8px", padding: "16px", marginBottom: "10px", borderLeft: "3px solid #38bdf8" }}>
                    <div style={{ color: "#38bdf8", fontSize: "0.8rem", marginBottom: "6px" }}>{c.clause_id} | Confidence: {Math.round(c.confidence * 100)}%</div>
                    <div style={{ color: "#e2e8f0", fontSize: "0.9rem" }}>{c.text}</div>
                    <div style={{ color: "#64748b", fontSize: "0.75rem", marginTop: "6px" }}>Keywords: {c.matched_keywords.join(", ")}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === "upload" && (
          <div>
            <div style={{ background: "#1e293b", borderRadius: "12px", padding: "24px", marginBottom: "20px" }}>
              <h3 style={{ margin: "0 0 8px", color: "#e2e8f0" }}>📤 Upload Document for Automatic Mapping</h3>
              <p style={{ color: "#94a3b8", marginBottom: "20px", fontSize: "0.9rem" }}>
                Upload any compliance document (PDF). The system will extract clauses using NLP
                and automatically map them to NIST CSF controls using TF-IDF similarity.
              </p>

              <div style={{ display: "flex", gap: "12px", alignItems: "center", flexWrap: "wrap" }}>
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  style={{
                    background: "#0f172a", color: "#e2e8f0", padding: "10px",
                    borderRadius: "8px", border: "1px solid #334155", fontSize: "0.85rem"
                  }}
                />
                <button onClick={handleUpload} disabled={!uploadFile || uploading}
                  style={{
                    background: uploadFile ? "#22c55e" : "#334155", color: "#0f172a",
                    padding: "10px 24px", borderRadius: "8px", border: "none",
                    cursor: uploadFile ? "pointer" : "not-allowed", fontWeight: "bold"
                  }}>
                  {uploading ? "⏳ Processing..." : "🚀 Upload & Auto-Map"}
                </button>
              </div>

              {uploadFile && (
                <p style={{ color: "#38bdf8", marginTop: "12px", fontSize: "0.85rem" }}>
                  Selected: {uploadFile.name}
                </p>
              )}
            </div>

            {uploadError && (
              <div style={{ background: "#7f1d1d", color: "#fca5a5", padding: "16px", borderRadius: "8px", marginBottom: "20px" }}>
                ⚠️ {uploadError}
              </div>
            )}

            {uploadResult && (
              <div>
                <div style={{
                  background: "#1e293b", borderRadius: "12px", padding: "20px", marginBottom: "20px",
                  display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px"
                }}>
                  <div>
                    <div style={{ fontSize: "1.8rem", fontWeight: "bold", color: "#38bdf8" }}>
                      {uploadResult.total_clauses_extracted}
                    </div>
                    <div style={{ color: "#94a3b8", fontSize: "0.8rem" }}>Clauses Extracted</div>
                  </div>
                  <div>
                    <div style={{ fontSize: "1.8rem", fontWeight: "bold", color: "#a78bfa" }}>
                      {uploadResult.total_mappings_created || uploadResult.mappings?.length || 0}
                    </div>
                    <div style={{ color: "#94a3b8", fontSize: "0.8rem" }}>Auto-Mappings Created</div>
                  </div>
                  <div>
                    <div style={{ fontSize: "1.8rem", fontWeight: "bold", color: "#22c55e" }}>
                      {uploadResult.average_mapping_confidence}%
                    </div>
                    <div style={{ color: "#94a3b8", fontSize: "0.8rem" }}>Avg Confidence</div>
                  </div>
                </div>

                <h4 style={{ color: "#e2e8f0", marginBottom: "12px" }}>Auto-Generated Mappings:</h4>
                {uploadResult.mappings?.map((m, i) => (
                  <div key={i} style={{
                    background: "#1e293b", borderRadius: "8px", padding: "16px",
                    marginBottom: "10px", borderLeft: "3px solid #22c55e"
                  }}>
                    <div style={{ color: "#94a3b8", fontSize: "0.85rem", marginBottom: "8px" }}>
                      <strong style={{ color: "#e2e8f0" }}>Extracted Text:</strong> {m.source_text}
                    </div>
                    <div style={{ display: "flex", gap: "16px", alignItems: "center", flexWrap: "wrap" }}>
                      <span style={{ color: "#38bdf8" }}>→ Mapped to: <strong>{m.matched_nist_control}</strong></span>
                      <span style={{ color: "#a78bfa" }}>{m.matched_nist_title}</span>
                      <span style={{
                        background: m.mapping_confidence > 0.7 ? "#14532d" : "#713f12",
                        color: m.mapping_confidence > 0.7 ? "#22c55e" : "#f59e0b",
                        padding: "2px 10px", borderRadius: "20px", fontSize: "0.8rem"
                      }}>
                        {Math.round(m.mapping_confidence * 100)}%
                      </span>
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
