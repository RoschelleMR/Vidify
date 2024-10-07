// import text_logo from '../assets/images/text_logo.png'
import vidify_black from '../assets/images/vidify_black.svg'

import { navLinks } from '../constants';
import { Link, useNavigate } from 'react-router-dom';

const Nav = () => {

    const navigate = useNavigate();

    const handleGoogleLogin = () => {
        // Redirect to Google OAuth on the backend for login
        if (localStorage.getItem("jwt")){
            navigate('/dashboard');
        }
        else{
            window.location.href = 'http://localhost:5000/auth/google';
        }
        
      };
    
      const handleGoogleSignUp = () => {
        // Redirect to Google OAuth on the backend for sign-up (same flow as login)
        window.location.href = 'http://localhost:5000/auth/google';
      };

    return(
        <header className='px-10 py-5'>
            <nav className='bg-slate-50 flex justify-between items-center py-2 px-6
            rounded-xl border border-slate-400'>
                <div className='flex justify-center items-center'>
                    <a href="#">
                        <img src={vidify_black} alt="Vidify Black Logo" width={40}/>
                    </a>
                    
                </div>

                
                <ul className='flex gap-6'>
                    {navLinks.map((item) => (
                        <li key={item.label}> 
                            <Link to={'/'+ (item.label).toLowerCase()}
                                href={item.href}
                                className='font-nav leading-normal text-body-base font-bold
                                 text-body-slate hover:text-black transition-all ease-in-out duration-200'
                            >
                                {item.label}
                            </Link>
                        </li>
                    ))}
                </ul>

                <div className='flex justify-center gap-4'>
                    <button onClick={handleGoogleLogin}  className='font-button leading-normal text-body-slate
                    font-bold text-body hover:text-black transition-all ease-in-out duration-500'>
                        Login
                    </button>
                    <button onClick={handleGoogleSignUp} className='flex justify-center font-bold text-body-default text-body-sm 
                    rounded-full px-4 py-1 bg-accent hover:bg-primary transition-all ease-in-out duration-500'>
                        Sign Up
                    </button>
                </div>
                
                
            </nav>
        </header>
    )
}

export default Nav