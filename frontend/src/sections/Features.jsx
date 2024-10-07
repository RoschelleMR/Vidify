
import { features } from '../constants';

const Features = () => {

    return(
        <section className="w-full flex flex-col 
        justify-center py-10 px-6
        gap-10 max-container">
            <div className="flex flex-col justify-center items-center gap-4 mt-10">
                <h2 className="text-heading-lg font-heading font-black text-center
                ">
                    Effortless Video Creation Powered by AI</h2>
                <p className="text-body-xl text-body-slate text-center
                ">
                    Transform Reddit posts into captivating videos in just a few clicks</p>
            </div>
            <div className="w-full flex justify-center">
                <ul className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10 '>
                    {features.map((feature) => (
                        <li key={feature.title} className="flex justify-center flex-col py-10 px-8
                        gap-3 bg-[#209b4b] rounded-2xl m-4 drop-shadow-xl flex-wrap">
                            <div className='bg-white flex justify-center p-4 w-fit rounded-xl'>
                                <img src={feature.icon} alt={feature.alt} width={25} 
                                className=''/>
                            </div>
                            <h3 className='font-body text-body-base font-bold text-body-alt'>{feature.title}</h3>
                            <p className='font-body text-body-sm text-body-alt leading-6'>{feature.description}</p>
                        </li>
                    ))}
                </ul>
            </div>
        </section>
    )
}

export default Features;