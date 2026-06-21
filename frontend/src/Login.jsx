import { useState } from "react"
import axios from "axios"

const API = "http://localhost:8001"

export default function Login({ onLogin }) {
  const [mode, setMode] = useState("login") // login | register
  const [form, setForm] = useState({ email: "", password: "", full_name: "", role: "viewer", organization: "" })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleLogin = async () => {
    setLoading(true)
    setError(null)
    try {
      const params = new URLSearchParams()
      params.append("username", form.email)
      params.append("password", form.password)
      const res = await axios.post(`${API}/auth/login`, params)
      const token = res.data.access_token
      localStorage.setItem("token", token)

      const meRes = await axios.get(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      onLogin(meRes.data, token)
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed")
    }
    setLoading(false)
  }

  const handleRegister = async () => {
    setLoading(true)
    setError(null)
    try {
      await axios.post(`${API}/auth/register`, form)
      setMode("login")
      setError(null)
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed")
    }
    setLoading(false)
  }

  const skipLogin = () => {
    onLogin({ email: "guest@viewer", full_name: "Guest Viewer", role: "viewer" }, null)
  }

  return (
    <div style={{
      fontFamily: "sans-serif", background: "#0f172a", minHeight: "100vh",
      display: "flex", alignItems: "center", justifyContent: "center", color: "white"
    }}>
      <div style={{ background: "#1e293b", borderRadius: "16px", padding: "40px", width: "400px", border: "1px solid #334155" }}>
        <div style={{ textAlign: "center", marginBottom: "24px" }}>
          <div style={{ fontSize: "2.5rem", marginBottom: "8px" }}>🛡️</div>
          <h2 style={{ margin: 0, color: "#38bdf8" }}>Compliance Mapping System</h2>
          <p style={{ color: "#94a3b8", fontSize: "0.85rem", marginTop: "4px" }}>
            University of Dhaka — PMICS Batch 4
          </p>
        </div>

        <div style={{ display: "flex", gap: "8px", marginBottom: "20px" }}>
          <button onClick={() => setMode("login")}
            style={{ flex: 1, padding: "10px", borderRadius: "8px", border: "none", cursor: "pointer", fontWeight: "bold",
              background: mode === "login" ? "#38bdf8" : "#0f172a", color: mode === "login" ? "#0f172a" : "#94a3b8" }}>
            Login
          </button>
          <button onClick={() => setMode("register")}
            style={{ flex: 1, padding: "10px", borderRadius: "8px", border: "none", cursor: "pointer", fontWeight: "bold",
              background: mode === "register" ? "#38bdf8" : "#0f172a", color: mode === "register" ? "#0f172a" : "#94a3b8" }}>
            Register
          </button>
        </div>

        {mode === "register" && (
          <>
            <input name="full_name" placeholder="Full Name" value={form.full_name} onChange={handleChange}
              style={inputStyle} />
            <select name="role" value={form.role} onChange={handleChange} style={inputStyle}>
              <option value="viewer">Viewer</option>
              <option value="auditor">Auditor</option>
              <option value="admin">Admin</option>
            </select>
            <input name="organization" placeholder="Organization" value={form.organization} onChange={handleChange}
              style={inputStyle} />
          </>
        )}

        <input name="email" type="email" placeholder="Email" value={form.email} onChange={handleChange}
          style={inputStyle} />
        <input name="password" type="password" placeholder="Password" value={form.password} onChange={handleChange}
          style={inputStyle} />

        {error && (
          <div style={{ background: "#7f1d1d", color: "#fca5a5", padding: "8px 12px", borderRadius: "8px", fontSize: "0.8rem", marginBottom: "12px" }}>
            ⚠️ {error}
          </div>
        )}

        <button onClick={mode === "login" ? handleLogin : handleRegister} disabled={loading}
          style={{ width: "100%", padding: "12px", borderRadius: "8px", border: "none", cursor: "pointer",
            background: "#22c55e", color: "#0f172a", fontWeight: "bold", fontSize: "0.95rem", marginBottom: "10px" }}>
          {loading ? "⏳ Processing..." : mode === "login" ? "Login" : "Create Account"}
        </button>

        <button onClick={skipLogin}
          style={{ width: "100%", padding: "10px", borderRadius: "8px", border: "1px solid #334155", cursor: "pointer",
            background: "transparent", color: "#94a3b8", fontSize: "0.85rem" }}>
          Continue as Guest (Viewer)
        </button>
      </div>
    </div>
  )
}

const inputStyle = {
  width: "100%", padding: "10px 12px", borderRadius: "8px", border: "1px solid #334155",
  background: "#0f172a", color: "#e2e8f0", marginBottom: "12px", fontSize: "0.9rem", boxSizing: "border-box"
}
