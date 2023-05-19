import React from 'react';
import './Homepage.css';
import { Navbar } from '../Navbar/Navbar';

export const HomePage = () => {
  return (
    <div className="home-page">
      <Navbar />
      <div className="home">
        <header className="home__header">
          <div className="header">
            <h1 className="title">Vacation Finder</h1>
            <div className="vacation-finder">
              <a className="vacation-finder__button" href="/vacationFinder">
                Get started!
              </a>
            </div>
          </div>
        </header>
      </div>
    </div>
  );
};
