import React, { useEffect, useState } from 'react';
import Navbar from './Navbar';
import EditMenuPopup from './EditMenuPopup'; // Import the popup component

const MenuPage = () => {
  const [menuData, setMenuData] = useState([]);
  const [currentMenu, setCurrentMenu] = useState(null);
  const [activeMenu, setActiveMenu] = useState(null);
  const [allReplyList, setAllReplyList] = useState([]);
  const [activeMenuName, setActiveMenuName] = useState("");
  const [isEditPopupOpen, setIsEditPopupOpen] = useState(false); // Popup visibility state
  const [selectedMenuId, setSelectedMenuId] = useState(null); // Selected menu ID for editing

    const fetchMenus = async () => {
      try {
        const response = await fetch('http://localhost:8000/menus');
        const data = await response.json();
        console.log(data);
  
        setMenuData(data);
  
        // Find the ID and name of the menu with active: true
        const activeMenu = data.find(menu => menu.active === true);
        const activeMenuId = activeMenu?.menu_id;
        const activeMenuName = activeMenu?.menu_name;
  
        // Set currentMenu to the ID of the active menu, or to the first menu's ID if none is active
        setActiveMenu(activeMenuId || (data[0] && data[0].menu_id));
        setActiveMenuName(activeMenuName || (data[0] && data[0].menu_name));
  
        return activeMenuId; // Return the active menu ID to use in the next fetch
      } catch (error) {
        console.error('Error fetching menu data:', error);
      }
    };
    const fetchAllReplyList = async (activeMenuId) => {
      try {
        const response = await fetch('http://localhost:8000/reply_lists');
        const data = await response.json();
        setAllReplyList(data);
  
        if (activeMenuId) {
          const associatedReplyList = data.filter(replyList =>
            replyList.menus.some(menu => menu.menu_id === activeMenuId)
          );
          setCurrentMenu(associatedReplyList || null);
        }
      } catch (error) {
        console.error('Error fetching reply list data:', error);
      }
    };
  
  useEffect(() => {
    const callFn = async () => {
      const activeMenuId = await fetchMenus();
      await fetchAllReplyList(activeMenuId);
    };
  
    callFn();
  }, []);

  const updateActiveMenu = async (menu_id) => {
    try {
      // Send the PUT request to update the active menu
      const response = await fetch(`http://localhost:8000/menus/${menu_id}/activate`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
      });
  
      if (!response.ok) throw new Error('Failed to update active menu');
  
      // Re-fetch menu data to get the latest active menu state
      await fetchMenus();
  
      // Update local state after fetching updated menu data
      setActiveMenu(menu_id);
      const activeMenuName = menuData.find(menu => menu.menu_id === menu_id)?.menu_name;
      setActiveMenuName(activeMenuName || (menuData[0] && menuData[0].menu_name));
  
      // Update current menu associated reply list based on the latest active menu
      const associatedReplyList = allReplyList.filter(replyList =>
        replyList.menus.some(menu => menu.menu_id === menu_id)
      );
      setCurrentMenu(associatedReplyList || null);
      
    } catch (error) {
      console.error('Error updating active menu:', error);
    }
  };
  

  const editPage = (menu_id) => {
    setSelectedMenuId(menu_id); // Set the selected menu ID
    setIsEditPopupOpen(true); // Open the edit popup
  };

  const closeEditPopup = () => {
    setIsEditPopupOpen(false); // Close the edit popup
  };

  return (
    <div className="flex h-screen w-screen">
      <Navbar />
      <main className="w-4/5 p-8 bg-gray-100">
        <header className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-bold">Menu Details</h2>
        </header>

        <div className="grid md:grid-cols-2 gap-6">
          <section className="bg-white p-6 rounded-lg shadow-lg">
            <h3 className="text-xl font-bold mb-4">Current Menu</h3>
            <div>
              <h4 className="font-semibold mb-2">{activeMenuName}</h4>
              <div className='grid grid-cols-3'>
                <div>
                  Item Name
                </div>
                <div>
                  Item Price
                </div>
                <div>
                  Available Quantity
                </div>
              </div>
              <ul className="space-y-3">
                {currentMenu?.map((item, index) => (
                  <li key={index} className="mt-4 grid grid-cols-3">
                    <span>{item.list_name}</span>
                    <button className="bg-yellow-50 text-gray-800 p-2 rounded-md w-20">₹{item.list_desc}</button>
                    {/* Items availability */}
                    <button>{item.available_quantity}</button>
                  </li>
                ))}
              </ul>
            </div>
          </section>

          <section className="bg-white p-6 rounded-lg shadow-lg">
            <h3 className="text-xl font-bold mb-4">Saved Menu</h3>
            <div className="space-y-4">
              {menuData.map((menu) => (
                <div key={menu.menu_id} className="flex justify-between items-center bg-yellow-50 p-3 rounded-lg">
                  <span>{menu.menu_name}</span>
                  <div className="flex space-x-2">
                    <button
                      className="bg-yellow-200 text-black p-2 rounded-md"
                      onClick={() => editPage(menu.menu_id)}
                    >
                      Edit
                    </button>
                    <button
                      className="bg-yellow-300 text-black p-2 rounded-md"
                      onClick={() => updateActiveMenu(menu.menu_id)}
                    >
                      Add to Chat
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      </main>

      {/* Conditionally render the EditMenuPopup when isEditPopupOpen is true */}
      {isEditPopupOpen && (
        <EditMenuPopup menuId={selectedMenuId} closePopup={closeEditPopup} onSave={() => fetchMenus()} />
      )}
    </div>
  );
};

export default MenuPage;
