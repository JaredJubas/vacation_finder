import React, { useState } from 'react';
import './CitiesList.css';

const CitiesList = ({ cities, isOpen }) => {
  const [sortOrder, setSortOrder] = useState(null);

  const toggleSortOrder = (header) => {
    if (sortOrder && sortOrder.header === header) {
      // If the header was already selected for sorting, toggle the order
      setSortOrder({
        header,
        order: sortOrder.order === 'asc' ? 'desc' : 'asc',
      });
    } else {
      // If a new header is selected for sorting, default to ascending order
      setSortOrder({ header, order: 'asc' });
    }
  };

  const sortCities = (cities, header, order) => {
    // Default sort order should be to sort cities in ascending order
    // On initial render, header and order will be undefined
    return cities.sort((a, b) => {
      if (header === 'temperature') {
        return order === 'desc'
          ? b.temperature - a.temperature
          : a.temperature - b.temperature;
      } else {
        return order === 'desc'
          ? b.city.localeCompare(a.city)
          : a.city.localeCompare(b.city);
      }
    });
  };

  const sortedCities = sortCities(cities, sortOrder?.header, sortOrder?.order);

  const citiesDropdownClasses = isOpen
    ? 'cities-dropdown-container cities-visible'
    : 'cities-dropdown-container';

  const getTooltipText = (header, sortOrder) => {
    const ascendingText = 'Sort ascending';
    const descendingText = 'Sort descending';

    if (header !== sortOrder?.header) {
      return ascendingText;
    }

    return sortOrder?.order === 'asc' ? descendingText : ascendingText;
  };

  const cityTooltip = getTooltipText('city', sortOrder);
  const temperatureTooltip = getTooltipText('temperature', sortOrder);

  return (
    <div className={citiesDropdownClasses}>
      <div className="cities-header">
        <div
          className="city-header"
          title={cityTooltip}
          onClick={() => toggleSortOrder('city')}
        >
          <span>City</span>
          {sortOrder?.header === 'city' && sortOrder.order === 'asc' && (
            <span className="arrow-up"></span>
          )}
          {sortOrder?.header !== 'city' && (
            <>
              <span className="arrow-up-down">
                <span className="arrow-up"></span>
                <span className="arrow-down"></span>
              </span>
            </>
          )}
          {sortOrder?.header === 'city' && sortOrder.order !== 'asc' && (
            <span className="arrow-down"></span>
          )}
        </div>
        <div
          className="average-header"
          title={temperatureTooltip}
          onClick={() => toggleSortOrder('temperature')}
        >
          <span>Average (°C)</span>
          {sortOrder?.header === 'temperature' && sortOrder.order === 'asc' && (
            <span className="arrow-up"></span>
          )}
          {sortOrder?.header !== 'temperature' && (
            <>
              <span className="arrow-up-down">
                <span className="arrow-up"></span>
                <span className="arrow-down"></span>
              </span>
            </>
          )}
          {sortOrder?.header === 'temperature' && sortOrder.order !== 'asc' && (
            <span className="arrow-down"></span>
          )}
        </div>
      </div>
      {sortedCities.map(({ city, temperature }) => {
        return (
          <div className="cities-container" key={city}>
            <div className="city-row">
              <div className="city">{city}</div>
              <div className="temperature">{temperature}</div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default CitiesList;
