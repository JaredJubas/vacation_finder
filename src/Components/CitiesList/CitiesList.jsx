import './CitiesList.css';

const CitiesList = ({ cities, isOpen }) => {
  const citiesSorted = cities.map(({ city }) => city).sort();

  const citiesDropdownClasses = isOpen
    ? 'cities-dropdown-container cities-visible'
    : 'cities-dropdown-container';

  return (
    <div className={citiesDropdownClasses}>
      <div className="cities-header">
        <div className="city-header">City</div>
        <div className="average-header">Average (°C)</div>
      </div>
      {citiesSorted.map((cityName) => {
        const cityData = cities.find(({ city }) => city === cityName);
        return (
          <div className="cities-container" key={cityData.city}>
            <div className="city-row">
              <div className="city">{cityData.city}</div>
              <div className="temperature">{cityData.temperature}</div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default CitiesList;
