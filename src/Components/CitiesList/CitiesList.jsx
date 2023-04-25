import React, { useState, useMemo } from 'react';
import './CitiesList.css';

const CitiesList = ({ cities, isOpen }) => {
  const [sortOrder, setSortOrder] = useState({ header: 'city', order: 'asc' });

  const toggleSortOrder = (header) => {
    setSortOrder((prevSortOrder) => {
      // If selected header is same as previously selected header then flip order
      // Otherwise default header to ascending
      const order =
        prevSortOrder.header === header
          ? prevSortOrder.order === 'asc'
            ? 'desc'
            : 'asc'
          : 'asc';
      return { header, order };
    });
  };

  const sortedCities = useMemo(() => {
    // Sort cities by header or temperature, depending on user selection
    // Default is to sort city names in ascending order
    const sorted = [...cities].sort((a, b) => {
      if (sortOrder.header === 'temperature') {
        return sortOrder.order === 'desc'
          ? b.temperature - a.temperature
          : a.temperature - b.temperature;
      } else {
        return sortOrder.order === 'desc'
          ? b.city.localeCompare(a.city)
          : a.city.localeCompare(b.city);
      }
    });
    return sorted;
  }, [cities, sortOrder]);

  const citiesDropdownClasses = isOpen
    ? 'cities-dropdown cities-dropdown--visible'
    : 'cities-dropdown';

  // Tooltip text so the user can see what will happen if you click a header
  const getTooltipText = (header) => {
    const ascendingText = 'Sort ascending';
    const descendingText = 'Sort descending';

    if (header !== sortOrder.header) {
      return ascendingText;
    }

    return sortOrder.order === 'asc' ? descendingText : ascendingText;
  };

  const cityTooltip = getTooltipText('city');
  const temperatureTooltip = getTooltipText('temperature');

  return (
    <div className={citiesDropdownClasses}>
      <div className="cities-dropdown-header">
        <div
          className="cities-dropdown-header__city-header"
          title={cityTooltip}
          onClick={() => toggleSortOrder('city')}
        >
          <span>City</span>
          {sortOrder.header === 'city' && sortOrder.order === 'asc' && (
            <span className="arrows__arrow-up"></span>
          )}
          {sortOrder.header !== 'city' && (
            <>
              <span className="arrows">
                <span className="arrows__arrow-up"></span>
                <span className="arrows__arrow-down"></span>
              </span>
            </>
          )}
          {sortOrder.header === 'city' && sortOrder.order !== 'asc' && (
            <span className="arrows__arrow-down"></span>
          )}
        </div>
        <div
          className="cities-dropdown-header__average-header"
          title={temperatureTooltip}
          onClick={() => toggleSortOrder('temperature')}
        >
          <span>Average (°C)</span>
          {sortOrder.header === 'temperature' && sortOrder.order === 'asc' && (
            <span className="arrows__arrow-up"></span>
          )}
          {sortOrder.header !== 'temperature' && (
            <>
              <span className="arrows">
                <span className="arrows__arrow-up"></span>
                <span className="arrows__arrow-down"></span>
              </span>
            </>
          )}
          {sortOrder.header === 'temperature' && sortOrder.order !== 'asc' && (
            <span className="arrows__arrow-down"></span>
          )}
        </div>
      </div>
      {sortedCities.map(({ city, temperature }) => {
        return (
          <div className="cities" key={city}>
            <div className="city-row">
              <div className="city-row__city">{city}</div>
              <div className="city-row__temperature">{temperature}</div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default CitiesList;
