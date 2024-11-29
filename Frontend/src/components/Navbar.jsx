import React from 'react';
import logout_icon from '../assets/logout_icon.png';
import DashboardIcon from '../assets/DashboardIcon.png';
import Order_icon from '../assets/Order_icon.png';
import customer_icon from '../assets/customer_icon.png';
// import Setting from '../assets/Setting.png';
import Menu_icon from '../assets/Menu_icon.png';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        console.log('User logged out');
        // Navigate to login page after logging out
        navigate('/');
    };
    const handleOrder = () => {
        console.log('Order details icon is clicked');
        // Navigate to Order Details page
        navigate('/orders');
    };
    const handleMenu = () => {
        console.log('Menu icon is clicked');
        // Navigate to Menu page
        navigate('/menu');
    };
    const handleCustomer = () => {
        console.log('Customers icon is clicked');
        // Navigate to Customers page
        navigate('/customers');
    };
    const handleDashboard = () => {
        console.log('Dashboard icon is clicked');
        // Navigate to Dashboard page
        navigate('/home');
    };
  return (
    <div className="h-screen w-1/5 flex bg-gray-50"> 
      <aside className="h-screen p-10">
        <h1 className="text-2xl text-dark-gray opacity-75 font-sans font-bold mb-6 flex justify-center items-center mt-7">BizBot</h1>
        <nav>
          <ul className="space-y-10 mt-12 ml-14">
            <li className=" text-light-gray font-medium flex items-center">
                <button onClick={handleDashboard} className="logout-btn flex">
              <img className='' src={DashboardIcon}></img>
              <div className='ml-3'>Dashboard</div>
              </button>
            </li>
            <li className=" text-light-gray font-medium flex items-center">
                <button onClick={handleOrder} className="logout-btn flex">
                <img className='' src={Order_icon}></img>
              <div className='ml-3'>Orders Detail</div>
                </button>
            </li>
            <li className=" text-light-gray font-medium flex items-center">
               <button onClick={handleMenu} className="logout-btn flex">
              <img className='' src={Menu_icon}></img>
              <div className='ml-3'>Menu</div>
              </button>
            </li>
            <li className=" text-light-gray font-medium flex items-center">
                <button onClick={handleCustomer} className="logout-btn flex">
                <img className='' src={customer_icon}></img>
                <div className='ml-3'>Customers</div>
                </button>
            </li>
            {/* <li className=" text-light-gray font-medium flex items-center">  
              <button onClick={handleLogout} className="logout-btn flex">
              <img className='' src={Setting}></img>
              <div className='ml-3'>Settings</div>
              </button>
            </li> */}
            <li className=" text-light-gray font-medium flex items-center">
                <button onClick={handleLogout} className="logout-btn flex">
                    <img className='' src={logout_icon}></img>
                    <div className='ml-3'>Logout</div>
                </button>
            </li>
          </ul>
        </nav>
      </aside>
    </div>
  )
}

export default Navbar
