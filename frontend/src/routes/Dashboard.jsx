import React, { useEffect, useState } from 'react';

import { useNavigate } from 'react-router-dom'

const Dashboard = () => {
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {

    const fetchData = async () => {
      const token = localStorage.getItem("jwt");
    
      if (!token) {
        navigate('/');  // Redirect to login if no token is present
        return;
      }
    
      try {
        const response = await fetch('http://localhost:5000/home', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
    
        if (response.status === 401) {
          // Token is expired or invalid, redirect to login
          localStorage.removeItem("jwt");
          navigate('/');
        } else {
          const data = await response.json();
          console.log(data);
          const message = 'Hello ' + data.given_name +  '!';
          setMessage(message || "Failed to fetch protected data");
        }
      } catch (error) {
        console.error('Error fetching protected data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      <p>{message}</p>
    </div>
  );
};

export default Dashboard;