import React, { useState, useEffect } from 'react';

const EditMenuPopup = ({ menuId, closePopup, onSave }) => {
  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState({ list_name: '', list_desc: '', available_quantity: '' });

  useEffect(() => {
    const fetchMenuItems = async () => {
      try {
        const response = await fetch(`http://localhost:8000/menus/${menuId}/items`);
        const data = await response.json();
        setItems(data);
      } catch (error) {
        console.error('Error fetching menu items:', error);
      }
    };

    fetchMenuItems();
  }, [menuId]);

  const handleItemChange = (index, key, value) => {
    const updatedItems = [...items];
    updatedItems[index][key] = value;
    setItems(updatedItems);
  };

  const addNewItem = () => {
    if (newItem.list_name && newItem.list_desc && newItem.available_quantity) {
      setItems([...items, { ...newItem }]);
      setNewItem({ list_name: '', list_desc: '', available_quantity: ''});
    }
  };

  const saveChanges = async () => {
    try {
      await fetch(`http://localhost:8000/menus/${menuId}/items`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ items }),
      });
      onSave();
      closePopup();
    } catch (error) {
      console.error('Error saving menu items:', error);
    }
  };

  return (
    <div className="fixed inset-0 bg-gray-800 bg-opacity-75 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
        <h2 className="text-2xl font-bold text-center mb-6">Edit Menu Items</h2>
       <div className="flex space-x-14">
        <div>Item Name</div>
        <div>Item Price</div>
        <div>Available Quantity</div>
        </div> 
        <ul className="space-y-4">
          {items.map((item, index) => (
            <li key={index} className="flex space-x-3">
              <input
                type="text"
                value={item.list_name}
                onChange={(e) => handleItemChange(index, 'list_name', e.target.value)}
                placeholder="Item Name"
                className="w-1/2 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
              />
              <input
                type="text"
                value={item.list_desc}
                onChange={(e) => handleItemChange(index, 'list_desc', e.target.value)}
                placeholder="Item Description"
                className="w-1/2 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
              />
              <input
                type="text"
                value={item.available_quantity}
                onChange={(e) => handleItemChange(index, 'available_quantity', e.target.value)}
                placeholder="Available Quantity"
                className="w-1/2 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
                />
            </li>
          ))}
        </ul>

        <div className="flex space-x-3 mt-6">
          <input
            type="text"
            value={newItem.list_name}
            onChange={(e) => setNewItem({ ...newItem, list_name: e.target.value })}
            placeholder="New Item Name"
            className="w-1/2 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
          />
          <input
            type="text"
            value={newItem.list_desc}
            onChange={(e) => setNewItem({ ...newItem, list_desc: e.target.value })}
            placeholder="New Item Price"
            className="w-1/2 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
          />
          {/* Available items */}
          <input
           type="text"
           value={newItem.available_quantity}
           onChange={(e) => setNewItem({ ...newItem, available_quantity: e.target.value })}
           placeholder="Available Quantity"
           className="w-1/2 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
          />
          <button 
            onClick={addNewItem} 
            className="bg-yellow-500 text-white px-4 py-2 rounded-md hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-500"
          >
            Add
          </button>
        </div>

        <div className="flex justify-end space-x-3 mt-8">
          <button 
            onClick={closePopup} 
            className="bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300"
          >
            Close
          </button>
          <button 
            onClick={saveChanges} 
            className="bg-yellow-500 text-white px-4 py-2 rounded-md hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-500"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
};

export default EditMenuPopup;
