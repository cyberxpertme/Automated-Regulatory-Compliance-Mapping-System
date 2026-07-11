import { useState, useEffect } from "react"
import axios from "axios"
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts"

const API = "http://localhost:8001"
const COLORS = ["#22c55e", "#f59e0b"]
const FN_COLORS = ["#38bdf8", "#a78bfa", "#22c55e", "#f59e0b", "#ec4899", "#06b6d4"]

export default function App({ user, token, onLogout }) {
  const [stats, setStats] = useState(null)
  const [analytics, setAnalytics] = useState(null)
  const [mappings, setMappings] = useState([])
  const [nlpResult, setNlpResult] = useState(null)
  const [activeTab, setActiveTab] = useState("dashboard")
  const [loading, setLoading] = useState(false)
  const [downloading, setDownloading] = useState(false)
  const [selectedFiles, setSelectedFiles] = useState([])
  const [uploadResult, setUploadResult] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState(null)
  const [liveStats, setLiveStats] = useState(null)
  const [downloadingUploadReport, setDownloadingUploadReport] = useState(false)
  const [history, setHistory] = useState(null)

  // Live Search states
  const [searchQuery, setSearchQuery] = useState("")
  const [searchResult, setSearchResult] = useState(null)
  const [searching, setSearching] = useState(false)
  const [isoSearch, setIsoSearch] = useState("")
  const [isoResult, setIsoResult] = useState(null)

  useEffect(() => {
    axios.get(`${API}/mapping/stats`).then(r => setStats(r.data)).catch(console.log)
    axios.get(`${API}/mapping/sample`).then(r => setMappings(r.data.mappings)).catch(console.log)
    axios.get(`${API}/search/analytics`).then(r => setAnalytics(r.data)).catch(console.log)
    fetchLiveStats()
  }, [])

  const fetchLiveStats = () => {
    axios.get(`${API}/upload/live-stats`).then(r => {
      if (r.data.has_data) setLiveStats(r.data)
    }).catch(console.log)
  }

  const fetchHistory = () => {
    axios.get(`${API}/upload/history`).then(r => setHistory(r.data)).catch(console.log)
  }

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
    } catch (err) { alert("Download failed: " + err.message) }
    setDownloading(false)
  }

  const handleFilesChange = (e) => {
    setSelectedFiles(Array.from(e.target.files))
    setUploadResult(null)
    setUploadError(null)
  }

  const handleMultiUpload = async () => {
    if (selectedFiles.length === 0) { setUploadError("Please select at least one file"); return }
    setUploading(true)
    setUploadError(null)
    const formData = new FormData()
    selectedFiles.forEach(f => formData.append("files", f))
    try {
      const res = await axios.post(`${API}/upload/analyze-multi`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      })
      setUploadResult(res.data)
      fetchLiveStats()
      fetchHistory()
    } catch (err) { setUploadError(err.response?.data?.detail || "Upload failed.") }
    setUploading(false)
  }

  const downloadUploadReport = async () => {
    setDownloadingUploadReport(true)
    try {
      const response = await axios.get(`${API}/upload/download-report`, { responseType: "blob" })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement("a")
      link.href = url
      link.setAttribute("download", `uploaded_analysis_${Date.now()}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (err) { alert("Download failed: " + (err.response?.data?.detail || err.message)) }
    setDownloadingUploadReport(false)
  }

  const handleLiveSearch = async () => {
    if (!searchQuery.trim()) return
    setSearching(true)
    try {
      const res = await axios.post(`${API}/search/map`, { query: searchQuery, top_n: 3 })
      setSearchResult(res.data)
    } catch (err) { console.log(err) }
    setSearching(false)
  }

  const handleIsoSearch = async () => {
    if (!isoSearch.trim()) return
    setSearching(true)
    try {
      const res = await axios.get(`${API}/search/iso/${isoSearch}`)
      setIsoResult(res.data)
    } catch (err) { console.log(err) }
    setSearching(false)
  }

  const pieData = stats ? [
    { name: "Full Coverage", value: stats.full_coverage },
    { name: "Partial Coverage", value: stats.partial_coverage },
  ] : []

  const barData = mappings.map(m => ({
    name: m.source_control_id,
    confidence: Math.round(m.confidence_score * 100),
  }))

  const liveFunctionData = liveStats?.function_distribution
    ? Object.entries(liveStats.function_distribution).map(([name, value]) => ({ name, value }))
    : []

  const analyticsBarData = analytics?.confidence_distribution
    ? Object.entries(analytics.confidence_distribution).map(([name, value]) => ({ name, value }))
    : []

  const fnBarData = analytics?.nist_function_breakdown
    ? Object.entries(analytics.nist_function_breakdown).map(([name, value]) => ({ name, value }))
    : []

  const TABS = [
    { id: "dashboard", label: "📊 Dashboard" },
    { id: "demo", label: "🎯 Live Demo" },
    { id: "mappings", label: "🗺️ Mappings" },
    { id: "nlp", label: "🧠 NLP Engine" },
    { id: "upload", label: "📤 Upload & Auto-Map" },
    { id: "history", label: "📋 History" },
  ]

  const confBadge = (score) => (
    <span style={{
      background: score >= 0.85 ? "#14532d" : score >= 0.70 ? "#713f12" : "#7f1d1d",
      color: score >= 0.85 ? "#22c55e" : score >= 0.70 ? "#f59e0b" : "#fca5a5",
      padding: "2px 10px", borderRadius: "20px", fontSize: "0.8rem", fontWeight: "bold"
    }}>
      {Math.round(score * 100)}%
    </span>
  )

  return (
    <div style={{ fontFamily: "sans-serif", background: "#0f172a", minHeight: "100vh", color: "white" }}>

      {/* Header */}
      <div style={{ background: "#1e293b", padding: "20px 40px", borderBottom: "1px solid #334155", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1 style={{ margin: 0, color: "#38bdf8", fontSize: "1.3rem" }}>🛡️ Automated Regulatory Compliance Mapping System</h1>
          <p style={{ margin: "4px 0 0", color: "#94a3b8", fontSize: "0.85rem" }}>University of Dhaka — PMICS Batch 4 | H-411 & H-392 | ISO 27001 + PCI-DSS → NIST CSF 2.0</p>
        </div>
        <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
          <div style={{ textAlign: "right" }}>
            <div style={{ color: "#e2e8f0", fontSize: "0.85rem", fontWeight: "bold" }}>{user?.full_name}</div>
            <div style={{ color: "#94a3b8", fontSize: "0.75rem" }}>{user?.role}</div>
          </div>
          <button onClick={onLogout} style={{ background: "#7f1d1d", color: "#fca5a5", padding: "8px 14px", borderRadius: "8px", border: "none", cursor: "pointer", fontSize: "0.8rem" }}>Logout</button>
          <button onClick={downloadReport} disabled={downloading}
            style={{ background: "#22c55e", color: "#0f172a", padding: "10px 20px", borderRadius: "8px", border: "none", cursor: "pointer", fontWeight: "bold", fontSize: "0.9rem" }}>
            {downloading ? "⏳ Generating..." : "📄 Download PDF Report"}
          </button>
        </div>
      </div>

      {/* Live Stats Banner */}
      {liveStats && (
        <div style={{ background: "#0c1e3e", padding: "10px 40px", fontSize: "0.85rem", color: "#94a3b8", borderBottom: "1px solid #1e3a5f" }}>
          🔴 Live: <strong style={{ color: "#38bdf8" }}>{liveStats.total_files}</strong> files |
          <strong style={{ color: "#38bdf8" }}> {liveStats.total_clauses_mapped}</strong> clauses |
          Confidence: <strong style={{ color: "#22c55e" }}>{liveStats.average_confidence}%</strong>
        </div>
      )}

      {/* Tabs */}
      <div style={{ display: "flex", gap: "8px", padding: "20px 40px 0", flexWrap: "wrap" }}>
        {TABS.map(tab => (
          <button key={tab.id}
            onClick={() => { setActiveTab(tab.id); if (tab.id === "history") fetchHistory() }}
            style={{ padding: "8px 20px", borderRadius: "8px", border: "none", cursor: "pointer", fontWeight: "bold",
              background: activeTab === tab.id ? "#38bdf8" : "#1e293b",
              color: activeTab === tab.id ? "#0f172a" : "#94a3b8" }}>
            {tab.label}
          </button>
        ))}
      </div>

      <div style={{ padding: "30px 40px" }}>

        {/* DASHBOARD */}
        {activeTab === "dashboard" && (
          <div>
            {stats && (
              <>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "16px", marginBottom: "24px" }}>
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
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px", marginBottom: "20px" }}>
                  <div style={{ background: "#1e293b", borderRadius: "12px", padding: "20px" }}>
                    <h3 style={{ margin: "0 0 16px", color: "#e2e8f0" }}>Coverage Breakdown</h3>
                    <ResponsiveContainer width="100%" height={200}>
                      <PieChart>
                        <Pie data={pieData} cx="50%" cy="50%" outerRadius={75} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                          {pieData.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                  <div style={{ background: "#1e293b", borderRadius: "12px", padding: "20px" }}>
                    <h3 style={{ margin: "0 0 16px", color: "#e2e8f0" }}>Confidence by Control</h3>
                    <ResponsiveContainer width="100%" height={200}>
                      <BarChart data={barData}>
                        <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 9 }} />
                        <YAxis tick={{ fill: "#94a3b8" }} domain={[0, 100]} unit="%" />
                        <Tooltip formatter={(v) => `${v}%`} />
                        <Bar dataKey="confidence" fill="#38bdf8" radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </>
            )}

            {analytics && (
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px", marginBottom: "20px" }}>
                <div style={{ background: "#1e293b", borderRadius: "12px", padding: "20px" }}>
                  <h3 style={{ margin: "0 0 16px", color: "#e2e8f0" }}>📊 Confidence Distribution</h3>
                  <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={analyticsBarData}>
                      <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 10 }} />
                      <YAxis tick={{ fill: "#94a3b8" }} />
                      <Tooltip />
                      <Bar dataKey="value" fill="#a78bfa" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <div style={{ background: "#1e293b", borderRadius: "12px", padding: "20px" }}>
                  <h3 style={{ margin: "0 0 16px", color: "#e2e8f0" }}>🎯 NIST Function Distribution</h3>
                  <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={fnBarData}>
                      <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 10 }} />
                      <YAxis tick={{ fill: "#94a3b8" }} />
                      <Tooltip />
                      <Bar dataKey="value" fill="#22c55e" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {liveStats && liveFunctionData.length > 0 && (
              <div style={{ background: "#1e293b", borderRadius: "12px", padding: "20px", border: "1px solid #38bdf8" }}>
                <h3 style={{ margin: "0 0 16px", color: "#38bdf8" }}>🔴 Live Upload — NIST Function Distribution</h3>
                <ResponsiveContainer width="100%" height={180}>
                  <PieChart>
                    <Pie data={liveFunctionData} cx="50%" cy="50%" outerRadius={70} dataKey="value" label={({ name, value }) => `${name}: ${value}`}>
                      {liveFunctionData.map((_, i) => <Cell key={i} fill={FN_COLORS[i % FN_COLORS.length]} />)}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        )}

        {/* LIVE DEMO TAB */}
        {activeTab === "demo" && (
          <div>
            <div style={{ background: "#1e293b", borderRadius: "12px", padding: "24px", marginBottom: "20px", border: "1px solid #38bdf8" }}>
              <h3 style={{ margin: "0 0 8px", color: "#38bdf8" }}>🎯 Live End-to-End Demo</h3>
              <p style={{ color: "#94a3b8", marginBottom: "20px", fontSize: "0.85rem" }}>
                Type any ISO control text or policy statement — system will run NLP extraction and TF-IDF matching live.
              </p>

              {/* Free text search */}
              <div style={{ marginBottom: "24px" }}>
                <label style={{ color: "#e2e8f0", fontSize: "0.9rem", fontWeight: "bold", display: "block", marginBottom: "8px" }}>
                  📝 Option 1: Enter any compliance text
                </label>
                <textarea
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  placeholder="e.g. A set of policies for information security shall be defined, approved by management, published and communicated to employees and relevant external parties."
                  rows={3}
                  style={{ width: "100%", padding: "12px", borderRadius: "8px", border: "1px solid #334155",
                    background: "#0f172a", color: "#e2e8f0", fontSize: "0.9rem", resize: "vertical", boxSizing: "border-box" }}
                />
                <button onClick={handleLiveSearch} disabled={searching || !searchQuery.trim()}
                  style={{ marginTop: "10px", background: "#38bdf8", color: "#0f172a", padding: "10px 24px",
                    borderRadius: "8px", border: "none", cursor: "pointer", fontWeight: "bold" }}>
                  {searching ? "⏳ Processing..." : "🚀 Run NLP + TF-IDF Mapping"}
                </button>
              </div>

              {/* ISO ID search */}
              <div style={{ borderTop: "1px solid #334155", paddingTop: "20px" }}>
                <label style={{ color: "#e2e8f0", fontSize: "0.9rem", fontWeight: "bold", display: "block", marginBottom: "8px" }}>
                  🔍 Option 2: Search by ISO Control ID
                </label>
                <div style={{ display: "flex", gap: "10px" }}>
                  <input
                    value={isoSearch}
                    onChange={e => setIsoSearch(e.target.value)}
                    placeholder="e.g. A.5.1 or A.8.7"
                    style={{ flex: 1, padding: "10px 14px", borderRadius: "8px", border: "1px solid #334155",
                      background: "#0f172a", color: "#e2e8f0", fontSize: "0.9rem" }}
                    onKeyDown={e => e.key === "Enter" && handleIsoSearch()}
                  />
                  <button onClick={handleIsoSearch} disabled={searching || !isoSearch.trim()}
                    style={{ background: "#a78bfa", color: "#0f172a", padding: "10px 24px",
                      borderRadius: "8px", border: "none", cursor: "pointer", fontWeight: "bold" }}>
                    {searching ? "⏳" : "🔍 Search"}
                  </button>
                </div>
                <p style={{ color: "#64748b", fontSize: "0.8rem", marginTop: "6px" }}>
                  Try: A.5.1, A.5.2, A.6.1, A.8.1, A.8.7, A.8.15
                </p>
              </div>
            </div>

            {/* Text search result */}
            {searchResult && (
              <div style={{ background: "#1e293b", borderRadius: "12px", padding: "24px", marginBottom: "20px" }}>
                <h4 style={{ color: "#38bdf8", margin: "0 0 20px" }}>🔄 Processing Steps</h4>

                {/* Step indicators */}
                <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "12px", marginBottom: "24px" }}>
                  {[
                    {
                      num: "1",
                      label: "Keyword Detection",
                      value: `${searchResult.processing_steps.step_1_keyword_detection.keyword_count} keywords found`,
                      detail: searchResult.processing_steps.step_1_keyword_detection.matched_keywords.join(", ") || "None",
                      color: "#38bdf8"
                    },
                    {
                      num: "2",
                      label: "NLP Processing",
                      value: `${searchResult.processing_steps.step_2_nlp_processing.sentence_count} sentence(s)`,
                      detail: searchResult.processing_steps.step_2_nlp_processing.is_compliance_clause ? "✅ Compliance clause detected" : "⚠️ No compliance keywords",
                      color: "#22c55e"
                    },
                    {
                      num: "3",
                      label: "TF-IDF Matching",
                      value: `${searchResult.processing_steps.step_3_tfidf_matching.corpus_size} NIST controls searched`,
                      detail: searchResult.processing_steps.step_3_tfidf_matching.method,
                      color: "#a78bfa"
                    }
                  ].map(step => (
                    <div key={step.num} style={{ background: "#0f172a", borderRadius: "10px", padding: "16px", borderLeft: `4px solid ${step.color}` }}>
                      <div style={{ color: step.color, fontWeight: "bold", marginBottom: "6px" }}>Step {step.num}: {step.label}</div>
                      <div style={{ color: "#e2e8f0", fontSize: "0.9rem", fontWeight: "bold" }}>{step.value}</div>
                      <div style={{ color: "#64748b", fontSize: "0.75rem", marginTop: "4px" }}>{step.detail}</div>
                    </div>
                  ))}
                </div>

                {/* Best match highlight */}
                {searchResult.best_match && (
                  <div style={{ background: "#14532d", borderRadius: "10px", padding: "16px", marginBottom: "16px", border: "1px solid #22c55e" }}>
                    <div style={{ color: "#22c55e", fontWeight: "bold", marginBottom: "8px", fontSize: "1rem" }}>
                      🏆 Best Match: {searchResult.best_match.nist_control_id}
                    </div>
                    <div style={{ color: "#e2e8f0", marginBottom: "6px" }}>{searchResult.best_match.nist_control_title}</div>
                    <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
                      {confBadge(searchResult.best_match.confidence_score)}
                      <span style={{ color: "#94a3b8", fontSize: "0.85rem" }}>Function: {searchResult.best_match.nist_function}</span>
                      <span style={{ color: searchResult.best_match.confidence_score >= 0.85 ? "#22c55e" : "#f59e0b", fontSize: "0.85rem" }}>
                        {searchResult.best_match.match_strength} Match
                      </span>
                    </div>
                  </div>
                )}

                {/* All top matches */}
                <h4 style={{ color: "#e2e8f0", margin: "0 0 12px" }}>Top {searchResult.top_nist_matches.length} NIST CSF Matches:</h4>
                {searchResult.top_nist_matches.map((m, i) => (
                  <div key={i} style={{ background: "#0f172a", borderRadius: "8px", padding: "14px", marginBottom: "8px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <div>
                      <div style={{ color: "#a78bfa", fontWeight: "bold", fontSize: "0.9rem" }}>{m.nist_control_id}</div>
                      <div style={{ color: "#e2e8f0", fontSize: "0.85rem" }}>{m.nist_control_title}</div>
                      <div style={{ color: "#64748b", fontSize: "0.75rem" }}>Function: {m.nist_function}</div>
                    </div>
                    <div style={{ textAlign: "right" }}>
                      {confBadge(m.confidence_score)}
                      <div style={{ color: "#94a3b8", fontSize: "0.75rem", marginTop: "4px" }}>{m.match_strength}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* ISO search result */}
            {isoResult && (
              <div style={{ background: "#1e293b", borderRadius: "12px", padding: "24px" }}>
                <h4 style={{ color: "#38bdf8", margin: "0 0 16px" }}>
                  🔍 ISO Control: {isoResult.source_control?.id}
                </h4>

                {/* Source control */}
                <div style={{ background: "#0f172a", borderRadius: "8px", padding: "16px", marginBottom: "16px", borderLeft: "4px solid #38bdf8" }}>
                  <div style={{ color: "#38bdf8", fontWeight: "bold", marginBottom: "6px" }}>📋 Source Control</div>
                  <div style={{ color: "#e2e8f0", fontWeight: "bold" }}>{isoResult.source_control?.title}</div>
                  <div style={{ color: "#94a3b8", fontSize: "0.85rem", marginTop: "6px" }}>{isoResult.source_control?.text}</div>
                  {isoResult.source_control?.category && (
                    <div style={{ color: "#64748b", fontSize: "0.75rem", marginTop: "4px" }}>Category: {isoResult.source_control.category}</div>
                  )}
                </div>

                {/* Pre-mapped result */}
                {isoResult.pre_mapped_result && (
                  <div style={{ background: "#14532d", borderRadius: "8px", padding: "16px", marginBottom: "16px", border: "1px solid #22c55e" }}>
                    <div style={{ color: "#22c55e", fontWeight: "bold", marginBottom: "8px" }}>✅ Pre-mapped NIST Control</div>
                    <div style={{ color: "#e2e8f0", fontWeight: "bold" }}>{isoResult.pre_mapped_result.nist_control_id} — {isoResult.pre_mapped_result.nist_control_title}</div>
                    <div style={{ display: "flex", gap: "12px", alignItems: "center", marginTop: "8px" }}>
                      {confBadge(isoResult.pre_mapped_result.confidence_score)}
                      <span style={{ color: "#94a3b8", fontSize: "0.85rem" }}>Function: {isoResult.pre_mapped_result.nist_function}</span>
                    </div>
                    <div style={{ color: "#94a3b8", fontSize: "0.8rem", marginTop: "6px" }}>
                      Gap: {isoResult.pre_mapped_result.gap_description}
                    </div>
                  </div>
                )}

                {/* Live TF-IDF verification */}
                {isoResult.live_tfidf_verification && (
                  <div>
                    <div style={{ color: "#a78bfa", fontWeight: "bold", marginBottom: "10px" }}>🔬 Live TF-IDF Verification (Top 3):</div>
                    {isoResult.live_tfidf_verification.map((m, i) => (
                      <div key={i} style={{ background: "#0f172a", borderRadius: "8px", padding: "12px", marginBottom: "8px", display: "flex", justifyContent: "space-between" }}>
                        <div>
                          <span style={{ color: "#a78bfa", fontWeight: "bold" }}>{m.nist_control_id}</span>
                          <span style={{ color: "#e2e8f0", fontSize: "0.85rem", marginLeft: "10px" }}>{m.nist_control_title}</span>
                        </div>
                        {confBadge(m.confidence_score)}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* MAPPINGS TAB */}
        {activeTab === "mappings" && (
          <div style={{ background: "#1e293b", borderRadius: "12px", overflow: "hidden", overflowX: "auto" }}>
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
                    <td style={{ padding: "12px 16px" }}>{confBadge(m.confidence_score)}</td>
                    <td style={{ padding: "12px 16px", color: "#94a3b8", fontSize: "0.8rem" }}>{m.gap_description || "✅ Full Match"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* NLP TAB */}
        {activeTab === "nlp" && (
          <div>
            <div style={{ background: "#1e293b", borderRadius: "12px", padding: "24px", marginBottom: "20px" }}>
              <h3 style={{ margin: "0 0 12px", color: "#e2e8f0" }}>🧠 NLP Clause Extraction Demo (TF-IDF Powered)</h3>
              <p style={{ color: "#94a3b8", marginBottom: "16px" }}>Click to run NLP extraction with TF-IDF similarity scoring on sample ISO 27001 text.</p>
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

        {/* UPLOAD TAB */}
        {activeTab === "upload" && (
          <div>
            <div style={{ background: "#1e293b", borderRadius: "12px", padding: "24px", marginBottom: "20px" }}>
              <h3 style={{ margin: "0 0 12px", color: "#e2e8f0" }}>📤 Upload Multiple Documents for Automatic Mapping</h3>
              <p style={{ color: "#94a3b8", marginBottom: "16px" }}>Select 2+ PDF or TXT compliance documents. System extracts clauses via NLP and maps to NIST CSF 2.0.</p>
              <div style={{ display: "flex", gap: "12px", alignItems: "center", marginBottom: "12px", flexWrap: "wrap" }}>
                <input type="file" accept=".pdf,.txt" multiple onChange={handleFilesChange}
                  style={{ color: "#e2e8f0", background: "#0f172a", border: "1px solid #334155", borderRadius: "8px", padding: "10px", fontSize: "0.85rem" }} />
                <button onClick={handleMultiUpload} disabled={uploading || selectedFiles.length === 0}
                  style={{ background: uploading ? "#475569" : "#22c55e", color: "#0f172a", padding: "10px 24px",
                    borderRadius: "8px", border: "none", cursor: uploading ? "not-allowed" : "pointer", fontWeight: "bold" }}>
                  {uploading ? "⏳ Analyzing..." : `🚀 Upload & Auto-Map (${selectedFiles.length})`}
                </button>
                {uploadResult && (
                  <button onClick={downloadUploadReport} disabled={downloadingUploadReport}
                    style={{ background: "#a78bfa", color: "#0f172a", padding: "10px 24px", borderRadius: "8px", border: "none", cursor: "pointer", fontWeight: "bold" }}>
                    {downloadingUploadReport ? "⏳ Generating..." : "📄 Download Combined Report"}
                  </button>
                )}
              </div>
              {selectedFiles.length > 0 && (
                <div style={{ color: "#38bdf8", fontSize: "0.85rem" }}>
                  📎 Selected ({selectedFiles.length}): {selectedFiles.map(f => f.name).join(", ")}
                </div>
              )}
              {uploadError && (
                <div style={{ background: "#7f1d1d", color: "#fca5a5", padding: "10px 16px", borderRadius: "8px", fontSize: "0.85rem", marginTop: "10px" }}>
                  ⚠️ {uploadError}
                </div>
              )}
            </div>
            {uploadResult && (
              <div>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "16px", marginBottom: "20px" }}>
                  {[
                    { label: "Files", value: uploadResult.combined_stats.total_files, color: "#38bdf8" },
                    { label: "Clauses Mapped", value: uploadResult.combined_stats.total_clauses_mapped, color: "#22c55e" },
                    { label: "Avg Confidence", value: `${uploadResult.combined_stats.average_confidence}%`, color: "#a78bfa" },
                    { label: "High Confidence", value: uploadResult.combined_stats.high_confidence_count, color: "#f59e0b" },
                  ].map(card => (
                    <div key={card.label} style={{ background: "#1e293b", borderRadius: "12px", padding: "16px", borderTop: `3px solid ${card.color}` }}>
                      <div style={{ fontSize: "1.6rem", fontWeight: "bold", color: card.color }}>{card.value}</div>
                      <div style={{ color: "#94a3b8", fontSize: "0.8rem" }}>{card.label}</div>
                    </div>
                  ))}
                </div>
                <div style={{ background: "#1e293b", borderRadius: "12px", overflow: "hidden", overflowX: "auto" }}>
                  <table style={{ width: "100%", borderCollapse: "collapse" }}>
                    <thead>
                      <tr style={{ background: "#0f172a" }}>
                        {["File", "Extracted Clause", "NIST Control", "Function", "Confidence"].map(h => (
                          <th key={h} style={{ padding: "10px 14px", textAlign: "left", color: "#38bdf8", fontSize: "0.8rem" }}>{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {uploadResult.mappings.slice(0, 50).map((m, i) => (
                        <tr key={i} style={{ borderTop: "1px solid #334155" }}>
                          <td style={{ padding: "10px 14px", color: "#64748b", fontSize: "0.75rem" }}>{m.source_file}</td>
                          <td style={{ padding: "10px 14px", color: "#e2e8f0", fontSize: "0.8rem", maxWidth: "280px" }}>{m.source_text}</td>
                          <td style={{ padding: "10px 14px", color: "#a78bfa", fontSize: "0.8rem", fontWeight: "bold" }}>{m.matched_nist_control}</td>
                          <td style={{ padding: "10px 14px", color: "#94a3b8", fontSize: "0.75rem" }}>{m.nist_function}</td>
                          <td style={{ padding: "10px 14px" }}>{confBadge(m.confidence_score)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* HISTORY TAB */}
        {activeTab === "history" && (
          <div>
            <div style={{ background: "#1e293b", borderRadius: "12px", padding: "24px", marginBottom: "20px" }}>
              <h3 style={{ margin: "0 0 8px", color: "#e2e8f0" }}>📋 Upload History</h3>
              <p style={{ color: "#94a3b8", margin: 0, fontSize: "0.85rem" }}>All past document analysis batches saved permanently in PostgreSQL.</p>
            </div>
            {!history ? (
              <div style={{ color: "#94a3b8", textAlign: "center", padding: "40px" }}>Loading history...</div>
            ) : history.total_batches === 0 ? (
              <div style={{ background: "#1e293b", borderRadius: "12px", padding: "40px", textAlign: "center", color: "#94a3b8" }}>
                No upload history yet. Go to Upload tab and analyze some documents.
              </div>
            ) : (
              <div>
                <div style={{ color: "#22c55e", marginBottom: "16px" }}>
                  📦 Total batches: <strong>{history.total_batches}</strong>
                </div>
                {history.history.map((batch, i) => (
                  <div key={i} style={{ background: "#1e293b", borderRadius: "12px", padding: "20px", marginBottom: "12px", border: "1px solid #334155" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
                      <div>
                        <span style={{ color: "#38bdf8", fontWeight: "bold" }}>Batch #{batch.upload_id}</span>
                        <span style={{ color: "#94a3b8", fontSize: "0.8rem", marginLeft: "12px" }}>
                          {batch.created_at ? new Date(batch.created_at).toLocaleString() : "N/A"}
                        </span>
                      </div>
                      <span style={{ background: "#14532d", color: "#22c55e", padding: "4px 12px", borderRadius: "20px", fontSize: "0.8rem" }}>Saved ✅</span>
                    </div>
                    <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "12px" }}>
                      {[
                        { label: "Files", value: batch.total_files, color: "#38bdf8" },
                        { label: "Clauses", value: batch.total_clauses_mapped, color: "#22c55e" },
                        { label: "Confidence", value: `${batch.average_confidence}%`, color: "#a78bfa" }
                      ].map(s => (
                        <div key={s.label} style={{ background: "#0f172a", borderRadius: "8px", padding: "12px" }}>
                          <div style={{ fontSize: "1.4rem", fontWeight: "bold", color: s.color }}>{s.value}</div>
                          <div style={{ color: "#94a3b8", fontSize: "0.75rem" }}>{s.label}</div>
                        </div>
                      ))}
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
