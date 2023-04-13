import React from 'react';
import './LocationList.css';
import CitiesList from '../CitiesList/CitiesList';

const showCities = (event) => {
  // TODO is there an easier way to access the elements?
  const parent = event.target.parentElement;
  const currentDisplay = parent.parentElement.lastChild.style.display;

  const caret = parent.children[2];

  if (currentDisplay === 'block') {
    // Hide the dropdown
    parent.parentElement.lastChild.style.display = 'none';

    // Rotate caret to point down
    caret.style.transform = 'rotate(0deg)';
  } else {
    // Show the dropdown
    parent.parentElement.lastChild.style.display = 'block';

    // Rotate caret to point up
    caret.style.transform = 'rotate(180deg)';
  }
};

const LocationList = ({ locations }) => {
  // Get a sorted list of countries so we can display it in alphabetical order
  const countries = Object.entries(locations).sort();

  const totalCities = countries.reduce((acc, curr) => {
    return acc + curr[1].length;
  }, 0);

  return (
    <div className="results-container">
      {totalCities > 0 ? (
        <div className="results-header">
          Found the following {totalCities} cities in {countries.length}{' '}
          countries. <br></br> Click each dropdown to view the cities in that
          country!
        </div>
      ) : (
        <div className="results-header">
          No cities found. Try changing the inputs and making another search!
        </div>
      )}
      <div className="countries-container">
        {countries.map(([country, cities]) => {
          const numCities = cities.length;
          const numCitiesText = numCities === 1 ? 'City' : 'Cities';
          return (
            <div className="country-dropdown-container" key={country}>
              <div
                className="country-dropdown"
                onClick={(event) => showCities(event)}
              >
                <div className="country">{country}</div>
                <div className="num-cities">
                  {numCities} {numCitiesText}
                </div>
                <div className="caret">
                  <div className="caret-left"></div>
                  <div className="caret-right"></div>
                </div>
              </div>
              {<CitiesList cities={cities}></CitiesList>}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default LocationList;
