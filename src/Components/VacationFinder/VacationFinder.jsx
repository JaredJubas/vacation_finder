import { useState } from 'react';
import axios from 'axios';
import './VacationFinder.css';
import Navbar from '../Navbar/Navbar';
import ErrorMessage from '../ErrorMessage/ErrorMessage';
import CountriesList from '../CountriesList/CountriesList';
import MonthDropdown from '../MonthDropdown/MonthDropdown';

const apiUrl = process.env.REACT_APP_API_URL;

const VacationFinder = () => {
  const [minTemp, setMinTemp] = useState(null);
  const [maxTemp, setMaxTemp] = useState(null);
  const [cityData, setCitiesData] = useState(null);
  const [firstTime, setFirstTime] = useState(true);
  const [errorMessage, setErrorMessage] = useState(null);
  const [month, setSelectedMonth] = useState(null);

  function getData(minTemp, maxTemp) {
    if (!minTemp || !maxTemp || !month) {
      setErrorMessage('Please fill out all search fields.');
      return;
    }

    setErrorMessage(null);

    // If apiUrl is not defined then it's on local
    const url = apiUrl ? `https://${apiUrl}/cities` : '/cities';

    axios({
      method: 'GET',
      url: url,
      params: {
        minTemp,
        maxTemp,
        month,
      },
    })
      .then(({ data }) => {
        setCitiesData(data);
        setFirstTime(false);
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          setErrorMessage('An error occurred. Please try again later.');
        }
      });
  }

  function handleMinTemp(event) {
    setMinTemp(event.target.value);
  }

  function handleMaxTemp(event) {
    setMaxTemp(event.target.value);
  }

  function handleSelectMonth(selectedMonth) {
    setSelectedMonth(selectedMonth);
  }

  return (
    <div className="vacation-page-container">
      <Navbar />

      <div className="vacation-finder-container">
        <div className="search-bar-container">
          {firstTime && (
            <p className="initial-message">
              Search for vacation destinations that works for you!
            </p>
          )}
          <ErrorMessage errorMessage={errorMessage} />
          <div className="search-container">
            <div className="search-components">
              <div className="min-temp-container">
                <label className="min-temp" htmlFor="minTemp">
                  Minimum Temperature
                </label>
                <input
                  type="text"
                  className="min-temp-input"
                  name="minTemp"
                  value={minTemp}
                  onChange={handleMinTemp}
                ></input>
              </div>
              <div className="max-temp-container">
                <label className="max-temp" htmlFor="maxTemp">
                  Maximum Temperature
                </label>
                <input
                  type="text"
                  className="max-temp-input"
                  name="maxTemp"
                  value={maxTemp}
                  onChange={handleMaxTemp}
                ></input>
              </div>
              <MonthDropdown onSelectMonth={handleSelectMonth} />
              <div className="submit-container">
                <button
                  onClick={() => getData(minTemp, maxTemp)}
                  className="submit-button"
                >
                  Search
                </button>
              </div>
            </div>
          </div>
        </div>
        {cityData && <CountriesList locations={cityData}></CountriesList>}
      </div>
    </div>
  );
};

export default VacationFinder;
