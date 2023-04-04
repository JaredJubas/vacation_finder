import { useState } from 'react';
import axios from 'axios';
import '../App.css';
import LocationList from '../location/locationList';

function HomePage() {
  const [minTemp, setMinTemp] = useState(null);
  const [maxTemp, setMaxTemp] = useState(null);
  const [cityData, setCitiesData] = useState(null);

  function getData() {
    const minTemp = document.getElementById('mintemp').value;
    const maxTemp = document.getElementById('maxtemp').value;
    const month = document.getElementById('month').value;

    axios({
      method: 'GET',
      url: '/cities',
      params: {
        minTemp,
        maxTemp,
        month
      }
    })
      .then((response) => {
        const res = response.data;
        setCitiesData(res);
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  }

  function handleMinTemp(event) {
    setMinTemp(event.target.value);
  }

  function handleMaxTemp(event) {
    setMaxTemp(event.target.value);
  }

  return (
    <div className="App">
      <header className="App-header">
        <div className="container">
          <label htmlFor="mintemp">Minimum Temperature: </label>
          <input
            type="text"
            id="mintemp"
            name="mintemp"
            placeholder="Mintemp"
            value={minTemp}
            onChange={handleMinTemp}></input>
          <br />
          <label htmlFor="maxtemp">Maximum Temperature: </label>
          <input
            type="text"
            id="maxtemp"
            name="maxtemp"
            placeholder="MaxTemp"
            value={maxTemp}
            onChange={handleMaxTemp}></input>
          <br />
          <label htmlFor="month">Month: </label>
          <select name="month" id="month" required>
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
          <br />
          <button
            onClick={() => getData(minTemp, maxTemp)}
            className="submitButton"
            disabled={minTemp === null || maxTemp === null}>
            Submit
          </button>
        </div>
        {cityData && (
          <LocationList
            location={cityData}
            month={document.getElementById('month').value}></LocationList>
        )}
      </header>
    </div>
  );
}

export default HomePage;
