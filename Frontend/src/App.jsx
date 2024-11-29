import React from 'react';
import {Routes, Route } from 'react-router-dom';
import LoginPage from './components/loginPage';
import LandingPage from './components/landingPage';
import OrderPage from './components/OrderPage'; 
import MenuPage from './components/MenuPage';
import NotFoundPage from './components/notFoundPage'; // Optional
import Customers from './components/Customers';
import './App.css';

function App() {
  return (
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/home" element={<LandingPage />} />
        <Route path="/orders" element={<OrderPage />} />
        <Route path="/menu" element={<MenuPage />} />
        <Route path="/customers" element={<Customers />} />
        <Route path="*" element={<NotFoundPage />} /> {/* Optional */}
      </Routes>
  );
}

export default App;
