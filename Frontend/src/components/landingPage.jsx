import React, { useState, useEffect } from 'react';
import Navbar from './Navbar';
import axios from 'axios'; 

const LandingPage = () => {
  // State for overview data and recent orders
  const [activeOrders, setActiveOrders] = useState([]);
  const [overviewData, setOverviewData] = useState({
    totalRevenue: 0,
    totalOrders: 0,
    totalCustomers: 0,
    date: 0,
  });
  const [recentOrders, setRecentOrders] = useState([]);

  useEffect(() => {
    // Fetch data when component mounts
    fetchOverviewData();
    fetchRecentOrders();
  }, []);

  const fetchOverviewData = async () => {
    try {
      const response = await axios.get('http://localhost:8000/overview'); // Replace with your backend endpoint
      setOverviewData(response.data);
    } catch (error) {
      console.error('Error fetching overview data:', error);
    }
  };

  const fetchRecentOrders = async () => {
    try {
      const activeResponse = await axios.get('http://localhost:8000/incomplete_orders');
      setActiveOrders(activeResponse.data);
    } catch (error) {
      console.error('Error fetching recent orders:', error);
    }
  };

  const renderOrders = (orders, isActive) => (
    orders.map(order => (
      <div key={order.order_id} className="grid grid-cols-6 gap-4 py-2 px-4 bg-yellow-50 rounded-md mb-2">
        <div>{order.items.map(item => `${item.item_name} (x${item.quantity})`).join(', ')}</div>
        <div>{`₹${order.grand_total}` || 'N/A'}</div>
        <div>{order.created_at}</div>
        <div>{order.user_inputs[0]?.user_name || 'N/A'}</div>
        <div>{order.user_inputs[0]?.address || 'N/A'}</div>
        <div>{order.ordered_by || 'N/A'}</div>
      </div>
    ))
  );

  return (
    <div className="min-h-screen flex">
      <Navbar />
      <main className="w-4/5 p-8 bg-gray-100">
        <header className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-bold">Overview</h2>
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

        {/* Overview Cards */}
        <section className="grid grid-cols-4 gap-4 mb-9">
          <div className="bg-white p-11 shadow rounded">
            <h3 className="text-lg font-bold">Today's Date</h3>
            <p className="text-2xl">{overviewData.date}</p>
          </div>
          <div className="bg-white p-11 shadow rounded">
            <h3 className="text-lg font-bold">Total Revenue</h3>
            <p className="text-2xl">₹{overviewData.totalRevenue}</p>
          </div>
          <div className="bg-white p-11 shadow rounded">
            <h3 className="text-lg font-bold">Total Orders</h3>
            <p className="text-2xl">{overviewData.totalOrders}</p>
          </div>
          <div className="bg-white p-11 shadow rounded">
            <h3 className="text-lg font-bold">Total Customers</h3>
            <p className="text-2xl">{overviewData.totalCustomers}</p>
          </div>
        </section>

        {/* Recent Orders */}
        <section className="bg-white p-6 shadow rounded mb-8">
          <h3 className="text-lg font-bold mb-4">Active Orders</h3>
          <div className="grid grid-cols-6 gap-4 font-semibold bg-yellow-300 p-2 px-4 mr-4 rounded-md">
            <div>Order Details</div>
            <div>Total Amount</div>
            <div>Date</div>
            <div>Customer Name</div>
            <div>Customer Address</div>
            <div>Customer Contact</div>
          </div>
            <div className="h-72 overflow-y-scroll mt-2">
            {renderOrders.length > 0 ? (renderOrders(activeOrders, true)) : (<div colSpan="3" className="p-4 text-center">
                    No recent orders available.
                  </div>)}
              </div>
            {/* <tbody> */}
             
              {/* {recentOrders.length > 0 ? (
                recentOrders.map((order) => (
                  <tr key={order.id}>
                    <td className="p-4">{order.details}</td>
                    <td className="p-4">{order.time}</td>
                    <td className="p-4">{order.status}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="3" className="p-4 text-center">
                    No recent orders available.
                  </td>
                </tr>
              )} */}
            {/* </tbody> */}
        </section>
      </main>
    </div>
  );
};

export default LandingPage;
