import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import HomePage from './Components/Home/HomePage';
import VacationFinder from './Components/VacationFinder/VacationFinder';

ReactDOM.render(
  <BrowserRouter basename={process.env.PUBLIC_URL}>
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/vacationFinder" element={<VacationFinder />} />
    </Routes>
  </BrowserRouter>,
  document.getElementById('root')
);
