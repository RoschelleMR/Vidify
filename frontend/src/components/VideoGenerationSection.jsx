import { useState } from "react";

const VideoGenerationSection = ({generateVideos, user}) => {
    const [subreddit, setSubreddit] = useState("");
    const [numVideos, setNumVideos] = useState(1);
    const [postType, setPostType] = useState("hot");
  
    const handleGenerateVideo = async () => {
      // Placeholder: Call backend API to generate videos
      console.log(`Generating ${numVideos} videos from r/${subreddit} (${postType} posts)`);

      generateVideos(subreddit, postType, numVideos, user);

    };
  
    return (
      <section className="flex flex-col gap-6 p-10 text-white w-full">
        <h2 className="font-extrabold text-heading-lg">Generate a New Video</h2>

        <div className="flex flex-col gap-10 ">
            {/* Subreddit Input */}
            <div className="flex flex-col gap-4">
                <label htmlFor="subreddit" className="text-heading-md">Subreddit Name</label>
                <input
                    type="text"
                    id="subreddit"
                    value={subreddit}
                    onChange={(e) => setSubreddit(e.target.value)}
                    className="bg-neutral-700 p-2 rounded text-white w-full"
                    placeholder="Enter subreddit name (e.g., funny, memes)"
                />
            </div>
    
            {/* Number of Videos Input */}
            <div className="flex flex-col gap-4">
            <label htmlFor="num-videos" className="text-heading-md">Number of Videos</label>
            <input
                type="number"
                id="num-videos"
                value={numVideos}
                onChange={(e) => setNumVideos(Number(e.target.value))}
                min="1"
                className="bg-neutral-700 p-2 rounded text-white w-full"
            />
            </div>
    
            {/* Post Type Dropdown */}
            <div className="flex flex-col gap-4">
            <label htmlFor="post-type" className="text-heading-md">Post Type</label>
            <select
                id="post-type"
                value={postType}
                onChange={(e) => setPostType(e.target.value)}
                className="bg-neutral-700 p-2 rounded text-white w-full"
            >
                <option value="hot">Hot</option>
                <option value="new">New</option>
                <option value="top">Top</option>
            </select>
            </div>
    
            {/* Generate Button */}
            <button
            onClick={handleGenerateVideo}
            className="bg-primary hover:bg-accent text-black font-bold
            py-2 px-4 rounded mt-4 max-w-max"
            >
            Generate Video
            </button>
        </div>
      </section>
    );
};
  
export default VideoGenerationSection;