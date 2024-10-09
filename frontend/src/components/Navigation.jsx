import {motion, useAnimationControls} from "framer-motion";
import { useEffect, useState } from "react";

import { useNavigate } from 'react-router-dom'

import {
    ChartBarIcon,
    ChartPieIcon,
    DocumentCheckIcon,
    Square2StackIcon,
    UsersIcon,
    ArrowLeftEndOnRectangleIcon
  } from "@heroicons/react/24/outline";

import NavigationLink from "./NavigationLink";


const containerVariants = {
    close: {
      width: "5rem",
      transition: {
        type: "spring",
        damping: 15,
        duration: 0.5,
      },
    },
    open: {
      width: "16rem",
      transition: {
        type: "spring",
        damping: 15,
        duration: 0.5,
      },
    },
  }

  const svgVariants = {
    close: {
      rotate: 360,
    },
    open: {
      rotate: 180,
    },
  }


const Navigation = ({user_data}) => {

    const [isOpen, setIsOpen] = useState(false)
    const navigate = useNavigate()

    const containerControls = useAnimationControls()
    const svgControls = useAnimationControls()

    // Function to handle logout
    const handleLogout = () => {
      // Clear the JWT from localStorage
      localStorage.removeItem("jwt");

      // Redirect to the login page
      navigate('/');
    };

    useEffect(() => {
        
        if (isOpen) {
          containerControls.start("open")
          svgControls.start("open")
        } else {
          containerControls.start("close")
          svgControls.start("close")
        }
      }, [containerControls, isOpen, svgControls])
    
      const handleOpenClose = () => {
        setIsOpen(!isOpen)
      }

    return (
        <motion.nav 
            variants={containerVariants}
            animate={containerControls}
            initial="close"
            className="bg-neutral-900 flex flex-col z-10 gap-20 p-5 absolute top-0 left-0 h-full shadow shadow-neutral-600"
        >
            <div className="flex flex-row w-full justify-between place-items-center">
                <div className="w-10 h-10 rounded-full">
                    <img src={user_data.picture} alt={user_data.name} referrerPolicy="no-referrer" />
                </div>
                <button 
                    className="p-1 rounded-full flex"
                    onClick={() => handleOpenClose()}>
                    <svg 
                        xmlns="http://www.w3.org/2000/svg" 
                        fill="none" 
                        viewBox="0 0 24 24" 
                        strokeWidth={2} 
                        stroke="currentColor" 
                        className="w-8 h-8 stroke-neutral-400">
                            <motion.path 
                                strokeLinecap="round" 
                                strokeLinejoin="round" 
                                variants={svgVariants}
                                animate={svgControls}
                                transition={
                                    {
                                        duration: 0.5,
                                        ease: "easeInOut"
                                    }
                                }
                                d="m5.25 4.5 7.5 7.5-7.5 7.5m6-15 7.5 7.5-7.5 7.5" 
                            />
                    </svg>
                </button>
            </div>
            <div className="flex flex-col gap-4">
                <NavigationLink name="Dashboard">
                    <ChartBarIcon className="stroke-inherit stroke-[0.75] min-w-8 w-8 size-8" />
                </NavigationLink>
                <NavigationLink name="Youtube Accounts ">
                    <UsersIcon className="stroke-inherit stroke-[0.75] min-w-8 w-8 size-8" />
                </NavigationLink>
                <div className="flex px-2 py-2 rounded cursor-pointer stroke-[0.75] hover:stroke-neutral-100
                stroke-neutral-400 text-neutral-400 hover:text-neutral-100 place-items-center gap-3 hover:bg-red-700/30 transition-colors duration-100"
                onClick={handleLogout}>
                    <ArrowLeftEndOnRectangleIcon className="stroke-inherit stroke-[0.75] min-w-8 w-8 size-8" />
                    <p className="text-inherit font-poppins overflow-hidden 
                    whitespace-nowrap tracking-wide">
                        Logout
                    </p>
                </div>
            </div>
            
        </motion.nav>
    );
};

export default Navigation;