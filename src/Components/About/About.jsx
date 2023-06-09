import React from 'react';
import './About.css';
import { Typography, Paper } from '@mui/material';
import { Navbar } from '../Navbar/Navbar';

export const About = () => {
  return (
    <div className="about-page">
      <Navbar />
      <Paper
        sx={{
          padding: 3,
          margin: 4,
        }}
      >
        <Typography variant="h4" gutterBottom sx={{ marginBottom: 2 }}>
          About Our Vacation City Finder
        </Typography>
        <Typography variant="body1" sx={{ marginBottom: 2 }}>
          Welcome to our Vacation City Finder! We&apos;re here to help you
          discover the perfect destinations for your next vacation based on your
          preferred weather conditions. Whether you&apos;re looking for a sunny
          beach getaway or a cozy winter retreat, our app has got you covered.
        </Typography>
        <Typography variant="h5" gutterBottom sx={{ marginBottom: 2 }}>
          How it Works
        </Typography>
        <Typography variant="body1" sx={{ marginBottom: 2 }}>
          Our app takes into account various factors to provide you with
          personalized recommendations. Simply input your desired minimum and
          maximum temperatures, select the month of your travel, and specify the
          maximum number of rainy days you&apos;re willing to tolerate. Our
          algorithm will search through our extensive database to find cities
          that match your criteria.
        </Typography>
        <Typography variant="body1" sx={{ marginBottom: 2 }}>
          We retrieve weather data from trusted sources such as Wikipedia,
          ensuring accuracy and reliability. Additionally, we prioritize your
          safety by using information from the Government of Canada&apos;s
          official site to exclude any countries that may pose potential risks.
        </Typography>
        <Typography variant="body1" sx={{ marginBottom: 2 }}>
          For precipitation data, we rely on the National Centers for
          Environmental Information (NCEI), which provides up-to-date and
          comprehensive information. This enables us to filter out cities that
          may experience excessive rainfall during your preferred travel period.
        </Typography>
        <Typography variant="h5" gutterBottom sx={{ marginBottom: 2 }}>
          Explore and Plan Your Dream Vacation
        </Typography>
        <Typography variant="body1" sx={{ marginBottom: 2 }}>
          Once you&apos;ve entered your criteria, our app will present you with
          a list of cities grouped by country. Clicking on a country will reveal
          the cities available within that region. Explore the options, view
          detailed weather information, and make an informed decision about your
          next vacation destination.
        </Typography>
        <Typography variant="body1" sx={{ marginBottom: 2 }}>
          We understand that planning a trip can be overwhelming, but with our
          Vacation City Finder, we aim to simplify the process and make it
          enjoyable for you. Let us help you create unforgettable memories in
          the perfect setting.
        </Typography>
        <Typography variant="h5" gutterBottom sx={{ marginBottom: 2 }}>
          Get Started Today
        </Typography>
        <Typography variant="body1" sx={{ marginBottom: 2 }}>
          Start using our Vacation City Finder now and unlock a world of
          possibilities. Find your ideal destination, pack your bags, and embark
          on a memorable journey. Happy vacation planning!
        </Typography>
      </Paper>
    </div>
  );
};
