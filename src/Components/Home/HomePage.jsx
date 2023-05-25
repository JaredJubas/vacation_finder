import React from 'react';
import { Button } from '@mui/material';
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
              <Button
                variant="contained"
                href="/vacationFinder"
                sx={{
                  borderRadius: '12px',
                  textTransform: 'none',
                  fontSize: '1rem',
                  padding: '10px 30px',
                }}
              >
                Get started!
              </Button>
            </div>
          </div>
        </header>
      </div>
    </div>
  );
};
