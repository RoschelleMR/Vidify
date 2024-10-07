import microphone from "../assets/icons/microphone.png";
import reddit from "../assets/icons/reddit.png";
import paragraph from "../assets/icons/paragraph.png";
import playButton from "../assets/icons/play-button.png";
import cloudUpload from "../assets/icons/cloud-upload.png";


export const navLinks = [
    { href: "#home", label: "Home" },
    { href: "#features", label: "Features" },
    { href: "#how-it-works", label: "How It Works" },
    { href: "#pricing", label: "Pricing" },
];

export const features = [
    {
        title: "AI-Generated Voiceovers",
        description: "Bring Reddit stories to life with natural-sounding AI voiceovers. No need for manual recording - the app handles it all for you",
        icon: microphone,
        alt: "Microphone icon"
    },
    {
        title: 'Seamless Subreddit Selection',
        description: 'Easily choose your favorite subreddits and transform posts into videos. The app lets you curate content from multiple sources effortlessly',
        icon: reddit,
        alt: "Reddit icon"
    },
    {
        title: 'Automated Video Creation',
        description: 'Generate high-quality videos automatically from Reddit posts. Simply pick your content, and the app does the heavy lifting',
        icon: playButton,
        alt: "Play button icon"
    },
    {
        title: 'Auto Upload to YouTube',
        description: 'Enjoy seamless auto uploads to your YouTube channel, letting your content go live without any manual effort',
        icon: cloudUpload,
        alt: "Cloud upload icon"
    },
    {
        title: 'Dynamic Captions',
        description: 'Your videos are enhanced with perfectly synced captions, dynamically generated to match the AI voiceover for maximum engagement',
        icon: paragraph,
        alt: "Paragraph icon"
    }
]
