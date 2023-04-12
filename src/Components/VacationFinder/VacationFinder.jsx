import { useState } from 'react';
import axios from 'axios';
import './VacationFinder.css';
import Navbar from '../Navbar/Navbar';
import ErrorMessage from '../ErrorMessage/ErrorMessage';
import LocationList from '../LocationList/LocationList';

const VacationFinder = () => {
  const [minTemp, setMinTemp] = useState(null);
  const [maxTemp, setMaxTemp] = useState(null);
  const [cityData, setCitiesData] = useState(null);
  const [firstTime, setFirstTime] = useState(true);

  function getData(minTemp, maxTemp) {
    const month = document.getElementsByClassName('month')[0].value;

    if (!minTemp || !maxTemp || !month) {
      document.getElementsByClassName('error-container')[0].style.display =
        'flex';
      return;
    } else {
      document.getElementsByClassName('error-container')[0].style.display =
        'none';
    }

    axios({
      method: 'GET',
      url: '/cities',
      params: {
        minTemp,
        maxTemp,
        month,
      },
    })
      .then((response) => {
        const res = response.data;
        setCitiesData(res);
        setFirstTime(false);
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
        }
      });
  }

  function handleMinTemp(event) {
    setMinTemp(event.target.value);
  }

  function handleMaxTemp(event) {
    setMaxTemp(event.target.value);
  }
  cityData;

  return (
    <div className="vacation-page-container">
      <Navbar />

      <div className="vacation-finder-container">
        {firstTime && (
          <p className="initial-message">
            Search for vacation destinations that works for you!
          </p>
        )}
        <ErrorMessage />
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
            <div className="month-container">
              <select className="month" id="month" required>
                <option value="" disabled selected>
                  Select a month
                </option>
                <option value="jan">January</option>
                <option value="feb">February</option>
                <option value="mar">March</option>
                <option value="apr">April</option>
                <option value="may">May</option>
                <option value="jun">June</option>
                <option value="jul">July</option>
                <option value="aug">August</option>
                <option value="sep">September</option>
                <option value="oct">October</option>
                <option value="nov">November</option>
                <option value="dec">December</option>
              </select>
            </div>
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
        {cityData && <LocationList locations={cityData}></LocationList>}
      </div>
    </div>
    // <div className="App">
    //   <header className="App-header">
    //     <div className="container">
    //       <label htmlFor="mintemp">Minimum Temperature: </label>
    //       <input
    //         type="text"
    //         id="mintemp"
    //         name="mintemp"
    //         placeholder="Mintemp"
    //         value={minTemp}
    //         onChange={handleMinTemp}
    //       ></input>
    //       <br />
    //       <label htmlFor="maxtemp">Maximum Temperature: </label>
    //       <input
    //         type="text"
    //         id="maxtemp"
    //         name="maxtemp"
    //         placeholder="MaxTemp"
    //         value={maxTemp}
    //         onChange={handleMaxTemp}
    //       ></input>
    //       <br />
    //       <label htmlFor="month">Month: </label>
    //       <select name="month" id="month" required>
    //         <option value="" disabled selected>
    //           Select a month
    //         </option>
    //         <option value="jan">January</option>
    //         <option value="feb">February</option>
    //         <option value="mar">March</option>
    //         <option value="apr">April</option>
    //         <option value="may">May</option>
    //         <option value="jun">June</option>
    //         <option value="jul">July</option>
    //         <option value="aug">August</option>
    //         <option value="sep">September</option>
    //         <option value="oct">October</option>
    //         <option value="nov">November</option>
    //         <option value="dec">December</option>
    //       </select>
    //       <br />
    //       <button
    //         onClick={() => getData(minTemp, maxTemp)}
    //         className="submitButton"
    //         disabled={minTemp === null || maxTemp === null}
    //       >
    //         Submit
    //       </button>
    //     </div>
    //     {cityData && <LocationList locations={cityData}></LocationList>}
    //   </header>
    // </div>
  );
};

export default VacationFinder;
