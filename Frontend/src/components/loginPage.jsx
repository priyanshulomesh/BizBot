import React, { useState } from 'react';
import background from '../assets/Landing_bg.png';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate(); 
    const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Username:', username);
    console.log('Password:', password);
    
    // Handle login logic here
    // navigating to landing page
    if (username && password) {
        // On successful login, navigate to the home page
        console.log('clicked', username, password);
        navigate('/home');
      }
    }
  return (
    <>
    <div className='absolute'>
        <img className='w-screen h-screen' src={background} alt='Background-Image'></img>
    </div>
    <div className='absolute z-10 h-screen w-screen bg-black opacity-50 place-content-center'>
    </div>
    <div className='absolute z-20 flex justify-center items-center h-screen w-screen border-2 border-gray-500'>
        <div className='flex-col bg-bgYellow w-1/4 h-1/2 flex items-center rounded-[16px] border-2 border-gray-500'>
          <h2 className='font-bold text-4xl p-12'>Login</h2>
          {/* Form */}
          <div className='-mt-6'>
          <form onSubmit={handleSubmit} className='w-full'>
            {/* Username field */}
            <div className='mb-4'>
              <input
                className='shadow appearance-none border rounded w-80 h-12 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
                id='username'
                type='text'
                placeholder='Username'
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>

            {/* Password field */}
            <div className='mb-12'>
              <input
                className='shadow appearance-none border rounded w-full h-12 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
                id='password'
                type='password'
                placeholder='Password'
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <div className='flex items-center justify-between'>
              <button
                className='h-11 bg-orange-500 hover:bg-custom-orange text-white font-bold py-2 px-4 rounded w-full focus:outline-none focus:shadow-outline'
                type='submit'
              >
                Login
              </button>
            </div>
          </form>
          </div>
        </div>
      </div>
    </>
    )
}

export default LoginPage
