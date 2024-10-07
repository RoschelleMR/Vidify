import HeroVideo from '../assets/videos/hero_section.webm'

const Hero = () => {

    return(
        <section id="home"
        className="w-full flex flex-col 
        justify-center min-h-screen
        gap-10 max-container">
            <div className="px-2 flex flex-col items-center">
                <h1 className="mt-10 mx-40 font-heading text-heading-xl font-black text-center leading-[1.2]">Turn Reddit Stories into Engaging Videos Automatically</h1>
                <p className="font-body font-medium text-body-slate text-body-xl
                leading-8 mt-8 text-center
                ">Easily convert Reddit posts into videos with captions, background clips, and auto-upload to YouTube</p>
                <button className='bg-primary flex justify-center font-body leading-normal font-bold
                    text-body-base text-body-default px-12 py-3 border-dashed border-2 border-black rounded-3xl mt-8 hover:bg-accent transition-all ease-in-out duration-500'>
                    Generate Your Video
                </button>
            </div>

            <video className="hero-video" autoPlay muted loop>
                <source src={HeroVideo} type="video/webm" />
                Your browser does not support the video tag.
            </video>

        </section>
    )
}

export default Hero