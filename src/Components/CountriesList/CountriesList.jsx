import React, { useState } from 'react';
import './CountriesList.css';
import CitiesList from '../CitiesList/CitiesList';

const CountriesList = ({ locations }) => {
  const [openDropdowns, setOpenDropdowns] = useState([]);

  const toggleDropdown = (country) => {
    setOpenDropdowns((prevOpenDropdowns) => {
      if (prevOpenDropdowns.includes(country)) {
        // If the country is already open, close it
        return prevOpenDropdowns.filter((c) => c !== country);
      } else {
        // If the country is closed, open it
        return [...prevOpenDropdowns, country];
      }
    });
  };

  // Get a sorted list of countries so we can display it in alphabetical order
  const countries = Object.entries(locations).sort();

  const totalCities = countries.reduce((acc, curr) => {
    return acc + curr[1].length;
  }, 0);

  return (
    <div className="results">
      {totalCities > 0 ? (
        <div className="results__header">
          Found the following {totalCities} cities in {countries.length}{' '}
          countries. <br />
          Click each dropdown to view the cities in that country!
        </div>
      ) : (
        <div className="results__header">
          No cities found. Try changing the inputs and making another search!
        </div>
      )}
      <div className="countries">
        {countries.map(([country, cities]) => {
          const numCities = cities.length;
          const numCitiesText = numCities === 1 ? 'City' : 'Cities';
          const isOpen = openDropdowns.includes(country);
          const dropdownClasses = isOpen
            ? 'country-dropdown bottom-flat'
            : 'country-dropdown';

          const caretClass = isOpen ? 'caret-up' : 'caret-down';

          return (
            <div className="countries__dropdown" key={country}>
              <div
                className={dropdownClasses}
                onClick={() => toggleDropdown(country)}
              >
                <span className="country">{country}</span>
                <span className="num-cities">
                  {numCities} {numCitiesText}
                </span>
                <span className={caretClass}></span>
              </div>
              {isOpen && (
                <CitiesList cities={cities} isOpen={isOpen}></CitiesList>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default CountriesList;
