import { useEffect, useState } from 'react';

const VideoList = ({ user }) => {
  const [videos, setVideos] = useState([]);

  // Fetch the user's videos from the backend (assuming a `/my_videos` route)
  useEffect(() => {
    const fetchVideos = async () => {
      const response = await fetch(`http://localhost:5000/my_videos?user_id=${user}`);
      const data = await response.json();
      setVideos(data.videos);
    };

    if (user) {
      fetchVideos();
    }
  }, [user]);

  // Function to delete a video
  const handleDelete = async (videoId, videoTitle) => {
    const response = await fetch(`http://localhost:5000/delete_video/${videoId}?user_id=${user}&blob_name=${videoTitle}`, {
      method: 'DELETE',
    });
    if (response.ok) {
      setVideos(videos.filter((video) => video.id !== videoId));  // Remove the deleted video from the list
    }
  };

  const handleUpload = async (videoId, videoPath, videoTitle, videoDesc, user_id) => {
    try {
      const response = await fetch('http://localhost:5000/upload_to_youtube', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_path: videoPath,
          title: videoTitle,
          description: videoDesc,
          user_id: user_id, 
        }),
      });
  
      const data = await response.json();
      if (data.status === 'success') {
        console.log('Video uploaded successfully!');
      } else {
        console.error('Error uploading video:', data.message);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  // Function to handle download
  const handleDownload = (videoUrl, videoTitle) => {
    const link = document.createElement('a');
    link.href = videoUrl;
    link.target = '_blank'; 
    link.rel = 'noopener noreferrer'; 
    link.setAttribute('download', `${videoTitle}.mp4`);  
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="flex flex-col gap-2 p-10 text-white w-full">
      <h2 className="font-extrabold text-heading-lg text-white mb-4">Your Generated Videos</h2>
      {videos.length > 0 ? (
        <ul className="space-y-4">
          {videos.map((video) => (
            <li
              key={video.id}
              className="flex justify-between items-center bg-neutral-800/30 p-4 rounded-lg shadow-lg"
            >
              <div className="text-white">
                <p className="font-bold">{video.title}</p>
              </div>
              <div className="flex space-x-4">
                <button
                  onClick={() => handleDownload(video.url)}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-3 rounded"
                >
                  Download
                </button>
                <button
                  onClick={() => handleUpload(video.id, video.url, video.title, 'Check out this video!', video.user_id)}
                  className="bg-green-500 hover:bg-green-700 text-white font-bold py-1 px-3 rounded"
                >
                  Upload
                </button>
                <button
                  onClick={() => handleDelete(video.id, video.title)}
                  className="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-3 rounded"
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-400">No videos generated yet.</p>
      )}
    </div>
  );
};

export default VideoList;
