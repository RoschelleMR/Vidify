import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'

import  Navigation  from '../components/Navigation'

const Dashboard = () => {
  const [message, setMessage] = useState("");
  const [userData, setUserData] = useState({});
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
          
          setUserData(data);

          console.log(data);

          const message = 'Hello ' + data.given_name +  '!';
          setMessage(message || "Failed to fetch protected data");
        }
      } catch (error) {
        console.error('Error fetching protected data:', error);
      }
    };

    fetchData();
  }, [navigate]);

  return (
    <main className='bg-dash relative flex'>
      {/* Sidebar */}
      <Navigation user_data={userData} />
      
      {/* Main area */}
      <section className="w-full flex flex-col 
      justify-center min-h-screen
      gap-10 px-10 ml-20">
        <h1 className='font-extrabold text-heading-xl text-white'>Dashboard</h1>
        <p className='font-body text-heading-md text-white'>{message}</p>
        <div className="w-full h-80 border border-neutral-500/50 bg-neutral-800/20 rounded" />
        <div className="flex flex-row gap-5 w-full">
          <div className="border-neutral-500/50 h-60 w-1/2 bg-neutral-800/20 rounded border" />
          <div className="border-neutral-500/50 h-60 w-1/2 bg-neutral-800/20 rounded border" />
        </div>
      </section>
    </main>
    
  );
}

export default Dashboard;