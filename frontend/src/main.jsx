import { StrictMode, useState } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import Login from './Login.jsx'
import './index.css'

function Root() {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem("token"))

  const handleLogin = (userData, jwtToken) => {
    setUser(userData)
    setToken(jwtToken)
  }

  const handleLogout = () => {
    localStorage.removeItem("token")
    setUser(null)
    setToken(null)
  }

  if (!user) {
    return <Login onLogin={handleLogin} />
  }

  return <App user={user} token={token} onLogout={handleLogout} />
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Root />
  </StrictMode>,
)
