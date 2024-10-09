import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'

import  Navigation  from '../components/Navigation'
import VideoGenerationSection from '../components/VIdeoGenerationSection';
import VideoList from '../components/VideoList';

async function generateVideos(subreddit, postType, numVideos, user) {
  
  const response = await fetch('http://localhost:5000/generate_videos', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      subreddit: subreddit,
      post_type: postType,
      num_videos: numVideos,
      user_id: user
    }),
  });

  const data = await response.json();
  console.log('Generated Videos:', data.generated_videos);
}

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
      gap-10 px-10 pt-8 ml-20">
        {/* Notice */}
        <div className='bg-yellow-700 rounded-2xl w-fit px-6 py-2'>
          <p className='font-body text-body-sm text-white text-center'>Automatic Scheduled Uploads Coming Soon!</p>
        </div>
        <h1 className='font-extrabold text-heading-xl text-white'>Dashboard</h1>
        <p className='font-body text-heading-md text-white'>{message}</p>

        
        <div className="w-full border border-neutral-500/50 bg-neutral-800/20 
        rounded flex flex-row justify-center gap-5 max-lg:flex-col">
          <VideoGenerationSection generateVideos = {generateVideos} user={userData.sub}/>
          <div className="w-full border border-neutral-500/50 bg-neutral-800/20 
        rounded flex flex-row justify-center gap-5">
            {/* Component to list all generated videos */}
            <VideoList user={userData.sub} />
          </div>
          
        </div>
        <div className="flex flex-row gap-5 w-full">
          <div className="border-neutral-500/50 h-60 w-1/2 bg-neutral-800/20 rounded border" />
          <div className="border-neutral-500/50 h-60 w-1/2 bg-neutral-800/20 rounded border" />
        </div>

      </section>
    </main>
    
  );
}

export default Dashboard;