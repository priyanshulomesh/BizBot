import React, { useState, useEffect } from 'react';
import Navbar from './Navbar'
import axios from 'axios';

const Customers = () => {
  const [customers, setCustomers] = useState([]);

  useEffect(() => {
    // Fetch orders data from backend when component mounts
    fetchCustomers();
  }, []);
  
  const fetchCustomers = async () => {
    try {
      // Fetch active orders
      const customersData = await axios.get('http://localhost:8000/user_profiles_with_inputs');
      setCustomers(customersData.data);
    } catch (error) {
      console.error('Error fetching orders:', error);
    }
  };
  const renderProfiles = (customers) => (
    customers.map(profile => (
      <div key={profile.id} className="grid grid-cols-5 gap-4 px-2 py-2 bg-yellow-50 rounded-md mb-2">
        {/* Customer ID */}
        <div>{profile.id}</div>
        {/* Customer Name */}
        <div>{profile.user_inputs[0]?.user_name || 'N/A'}</div>
        {/* Customer Phone */}
        <div>{profile.user_phone_number}</div>
        {/* Customer Address */}
        <div>{profile.user_inputs[0]?.user_Address || 'N/A'}</div>
        {/* Created Date & Time */}
      <div>
        {new Date(profile.created_at).toLocaleDateString()}{", "}
        {new Date(profile.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </div>
      </div>
    ))
  );
  
  return (
    <div className="flex h-screen w-screen">
      <Navbar />
      <main className="w-4/5 p-8 bg-gray-100">
        <header className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-bold">Customers</h2>
          {/* <div className="flex items-center space-x-4">
            <input
              type="text"
              placeholder="Search..."
              className="border p-2 rounded"
            />
            <img
              src="https://via.placeholder.com/40"
              alt="User"
              className="rounded-full"
            />
          </div> */}
        </header>

        {/* Active Orders Section */}
        <div className="bg-white p-3 rounded-lg shadow-md mb-2">
          <h2 className="text-2xl font-bold mb-4">Customer Information</h2>
          <div className="grid grid-cols-5 gap-4 font-semibold bg-yellow-300 p-2 mr-4 rounded-md">
            <div>Customer Id</div>
            <div>Name</div>
            <div>Phone No.</div>
            <div>Address</div>
            <div>Profile Created at</div>
          </div>
          <div className="h-96 overflow-y-scroll mt-2">
            {renderProfiles(customers)}
          </div>
        </div>
      </main>
    </div>
  )
}

export default Customers
