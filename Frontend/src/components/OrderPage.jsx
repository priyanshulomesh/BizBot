import React, { useState, useEffect } from 'react';
import Navbar from './Navbar';
import axios from 'axios';


const OrderPage = () => {
  const [activeOrders, setActiveOrders] = useState([]);
  const [previousOrders, setPreviousOrders] = useState([]);
  const [orderStatus, setOrderStatus] = useState({});

  useEffect(() => {
    // Fetch orders data from backend when component mounts
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      // Fetch active orders
      const activeResponse = await axios.get('http://localhost:8000/incomplete_orders');
      setActiveOrders(activeResponse.data);

      // Fetch previous orders
      const previousResponse = await axios.get('http://localhost:8000/complete_orders');
      setPreviousOrders(previousResponse.data);
    } catch (error) {
      console.error('Error fetching orders:', error);
    }
  };

  const handleStatusChange = (orderId, newStatus) => {
    setOrderStatus({ ...orderStatus, [orderId]: newStatus });

    // Call API to update the status
    axios.put(`http://localhost:8000/api/orders/${orderId}/status`, { status: newStatus })
      .then(() => {
        console.log(`Status updated for order ${orderId}`);
        // Re-fetch the orders to get the latest data
        fetchOrders();
      })
      .catch(error => {
        console.error('Error updating status:', error);
      });
  };

  const renderOrders = (orders, isActive) => (
    orders.map(order => (
      <div key={order.order_id} className="grid grid-cols-7 gap-4 py-2 bg-yellow-50 px-4 rounded-md mb-2">
        <div>{order.items.map(item => `${item.item_name} (x${item.quantity})`).join(', ')}</div>
        <div>{`₹${order.grand_total}` || 'N/A'}</div>
        <div>{order.created_at}</div>
        <div>{order.user_inputs[0]?.user_name || 'N/A'}</div>
        <div>{order.user_inputs[0]?.address || 'N/A'}</div>
        <div>{order.ordered_by || 'N/A'}</div>
        <div>
          {isActive ? (
            <select
              className="block w-full bg-gray-50 border border-gray-300 rounded-md py-2 px-3 text-gray-700 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              value={orderStatus[order.order_id] || order.order_status}
              onChange={(e) => handleStatusChange(order.order_id, e.target.value)}
            >
              {/* <option value="Placed">Placed</option>
              <option value="Prepared">Prepared</option>
              <option value="Transit">Transit</option> */}
              <option value="In Progress">In Progress</option>
              <option value="Delivered">Delivered</option>
              <option value="Cancelled">Cancelled</option>
            </select>
          ) : (
            <div>
                {order.order_status === 'yes' ? 'Completed' : 
                order.order_status === 'cancel' ? 'Cancelled' : 
                order.order_status}
            </div>
            
            // <div>Completed</div>
          )}
        </div>
      </div>
    ))
  );

  return (
    <div className="flex h-screen w-screen">
      <Navbar />
      <main className="w-4/5 p-8 bg-gray-100">
        <header className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-bold">Order Details</h2>
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
          <h2 className="text-2xl font-bold mb-4">Active Orders</h2>
          <div className="grid grid-cols-7 gap-4 font-semibold bg-yellow-300 p-2 mr-4 px-4 rounded-md">
            <div>Order Details</div>
            <div>Total Amount</div>
            <div>Date</div>
            <div>Customer Name</div>
            <div>Customer Address</div>
            <div>Customer Contact</div>
            <div>Order Status</div>
          </div>
          <div className="h-48 overflow-y-scroll mt-2">
            {renderOrders(activeOrders, true)}
          </div>
        </div>

        {/* Previous Orders Section */}
        <div className="bg-white p-3 rounded-lg shadow-md">
          <h2 className="text-2xl font-bold mb-4">Previous Orders</h2>
          <div className="grid grid-cols-7 gap-4 font-semibold bg-yellow-300 p-2 mr-4 px-4 rounded-md">
            <div>Order Details</div>
            <div>Total Amount</div>
            <div>Date</div>
            <div>Customer Name</div>
            <div>Customer Address</div>
            <div>Customer Contact</div>
            <div>Order Status</div>
          </div>
          <div className="h-48 overflow-y-scroll mt-2">
            {renderOrders(previousOrders, false)}
          </div>
        </div>
      </main>
    </div>
  );
};

export default OrderPage;
