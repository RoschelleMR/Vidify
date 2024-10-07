import React, { useEffect, useState } from 'react';

const Dashboard = () => {
  const [message, setMessage] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("jwt");

    // Fetch protected data from the backend
    const fetchData = async () => {
      const response = await fetch('http://localhost:5000/home', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      const data = await response.json();
      console.log(data);
      const message = 'Hello ' + data.given_name +  '!';
      setMessage(message || "Failed to fetch protected data");
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