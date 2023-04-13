import React from 'react';
import './LocationList.css';
import CitiesList from '../CitiesList/CitiesList';

const showCities = (event) => {
  const parent = event.target.parentElement;
  const currentDisplay = parent.parentElement.lastChild.style.display;

  // const caretDown = parent.children[2];
  // const caretUp = parent.children[3];

  if (currentDisplay === 'block') {
    parent.parentElement.lastChild.style.display = 'none';

    // caretUp.style.display = 'none';
    // caretDown.style.display = 'block';
  } else {
    parent.parentElement.lastChild.style.display = 'block';

    // caretDown.style.display = 'none';
    // caretUp.style.display = 'block';
  }
};

const LocationList = ({ locations }) => {
  const countries = Object.entries(locations).sort();
  const totalCities = countries.reduce((acc, curr) => {
    return acc + curr[1].length;
  }, 0);

  return (
    <div className="results-container">
      <div className="results-header">
        Found the following {totalCities} cities in {countries.length}{' '}
        countries. <br></br> Click each dropdown to view the cities in that
        country!
      </div>
      <div className="countries-container">
        {countries.map(([country, cities]) => {
          const numCities = cities.length;
          const numCitiesText = numCities === 1 ? 'City' : 'Cities';
          return (
            <div
              className="country-dropdown-container"
              key={country}
              onClick={(event) => showCities(event)}
            >
              <div className="country-dropdown">
                <div className="country">{country}</div>
                <div className="num-cities">
                  {numCities} {numCitiesText}
                </div>
                <div className="caret-down">
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
