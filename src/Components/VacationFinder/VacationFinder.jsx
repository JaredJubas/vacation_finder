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

    // Check if minTemp and maxTemp are valid numbers
    if (isNaN(parseFloat(minTemp)) || isNaN(parseFloat(maxTemp))) {
      setErrorMessage('Please enter valid temperature values.');
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
    <div className="vacation-page">
      <Navbar />

      <div className="vacation-page__finder">
        <div className="vacation-page__search-bar">
          {firstTime && (
            <p className="vacation-page__message">
              Search for vacation destinations that works for you!
            </p>
          )}
          <ErrorMessage errorMessage={errorMessage} />
          <div className="vacation-page__search">
            <div className="vacation-page__search-components">
              <div className="vacation-page__min-temp">
                <label
                  className="vacation-page__temp-label"
                  htmlFor="vacation-page__min-temp-input"
                >
                  Minimum Temperature
                </label>
                <input
                  type="text"
                  id="vacation-page__min-temp-input"
                  name="minTemp"
                  value={minTemp}
                  onChange={handleMinTemp}
                ></input>
              </div>
              <div className="vacation-page__max-temp">
                <label
                  className="vacation-page__temp-label"
                  htmlFor="vacation-page__max-temp-input"
                >
                  Maximum Temperature
                </label>
                <input
                  type="text"
                  id="vacation-page__max-temp-input"
                  name="maxTemp"
                  value={maxTemp}
                  onChange={handleMaxTemp}
                ></input>
              </div>
              <MonthDropdown onSelectMonth={handleSelectMonth} />
              <div className="vacation-page__submit">
                <button
                  onClick={() => getData(minTemp, maxTemp)}
                  className="vacation-page__submit-button"
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
