import { useEffect, useState } from 'react'
import './App.css'
import axios from 'axios'

import { Routes, Route, Navigate, useNavigate } from 'react-router-dom'

import Dashboard from './routes/Dashboard'
import Home from './routes/Home'


function App() {

  const [jwt, setJwt] = useState(localStorage.getItem("jwt"));
  const navigate = useNavigate();

  useEffect(() => {
    // Check if JWT exists in the URL after Google login
    const query = new URLSearchParams(window.location.search);
    const token = query.get("jwt");

    if (token) {
      setJwt(token);
      localStorage.setItem("jwt", token);  // Store JWT for future use
      window.history.replaceState(null, null, window.location.pathname);  // Clean up the URL

      // Navigate to the dashboard after login/signup
      navigate('/dashboard');
    }
  }, [navigate]);

  return (
    <div >

      <Routes>
        {/* Route for Dashboard (Protected Route) */}
        <Route
          path="/dashboard"
          element={jwt ? <Dashboard /> : <Navigate to="/" />}  // Redirect to home if not authenticated
        />
        
        {/* Route for Home (with login and sign-up buttons) */}
        <Route path="/" element={<Home />} />
        
      </Routes>
    </div>
  )
}

export default App
