import React from 'react';
import './Navbar.css';

export const Navbar = () => {
  return (
    <nav className="navbar">
      <ul className="navbar__links">
        <li className="navbar__item">
          <a href="/" className="navbar__item navbar__title">
            Home
          </a>
        </li>
        <li className="navbar__item">
          <a href="/vacationFinder" className="navbar__item">
            Vacation Finder
          </a>
        </li>
      </ul>
    </nav>
  );
};
