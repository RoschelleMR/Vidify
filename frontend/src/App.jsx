import { useEffect, useState } from 'react'
import './App.css'

import { Routes, Route, Navigate, useNavigate } from 'react-router-dom'
import { jwtDecode } from "jwt-decode";

import Dashboard from './routes/Dashboard'
import Home from './routes/Home'


function App() {

  const [jwt, setJwt] = useState(localStorage.getItem('jwt'));
  const navigate = useNavigate();

  useEffect(() => {
    // Extract JWT from the URL after Google login
    const query = new URLSearchParams(window.location.search);
    const token = query.get('jwt');

    if (token) {
      setJwt(token);
      localStorage.setItem('jwt', token);  // Store JWT in localStorage

      // Check if JWT has expired
      const decodedToken = jwtDecode(token);
      const currentTime = Date.now() / 1000;

      if (decodedToken.exp < currentTime) {
        // Token is expired, remove it and redirect to login
        localStorage.removeItem('jwt');
        navigate('/');
      } else {
        // Token is valid, redirect to dashboard
        navigate('/dashboard');
      }
    }
  }, [navigate]);

  return (
    <div>

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
