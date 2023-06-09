import React, { useState } from 'react';
import './Navbar.css';

export const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <nav className={`navbar ${menuOpen ? 'menu-open' : ''}`}>
      <div className="navbar__container">
        <div className="navbar__menu-icon" onClick={toggleMenu}>
          <div className="navbar__menu-icon-bar"></div>
          <div className="navbar__menu-icon-bar"></div>
          <div className="navbar__menu-icon-bar"></div>
        </div>
        <ul className={`navbar__links ${menuOpen ? 'menu-open' : ''}`}>
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
          <li className="navbar__item">
            <a href="/about" className="navbar__item">
              About
            </a>
          </li>
        </ul>
      </div>
      {menuOpen && <div className="navbar__overlay" onClick={toggleMenu}></div>}
    </nav>
  );
};
