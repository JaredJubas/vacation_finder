import React, { useState, useEffect } from 'react';
import axios from 'axios';
import * as MUI from '@mui/material';
import './VacationFinder.css';
import { Navbar } from '../Navbar/Navbar';
import { ErrorMessage } from '../ErrorMessage/ErrorMessage';
import { CountriesList } from '../CountriesList/CountriesList';
import { MONTHS } from '../../utils/months';

const apiUrl = process.env.REACT_APP_API_URL;

export const VacationFinder = () => {
  const [minTemp, setMinTemp] = useState(''),
    [maxTemp, setMaxTemp] = useState(''),
    [cityData, setCitiesData] = useState(null),
    [firstTime, setFirstTime] = useState(true),
    [errorMessage, setErrorMessage] = useState(''),
    [open, setOpen] = useState(false),
    [month, setSelectedMonth] = useState('');

  // For some reason, when the month dropdown is selected and cities are loaded, padding is being
  // added to the right and the srollbar disappears
  useEffect(() => {
    // TODO This is a temporary solution. Figure out why padding is being added when the month
    // dropdown is selected
    if (open) {
      document.body.classList.add('dropdown-open');
    } else {
      document.body.classList.remove('dropdown-open');
    }

    return () => {
      document.body.classList.remove('dropdown-open');
    };
  }, [open]);

  function getData(minTemp, maxTemp) {
    if (!minTemp || !maxTemp || !month) {
      setErrorMessage('Please fill out all search fields.');
      return;
    }

    const floatMinTemp = parseFloat(minTemp);
    const floatMaxTemp = parseFloat(maxTemp);

    // Check if minTemp > maxTemp
    if (floatMinTemp > floatMaxTemp) {
      setErrorMessage(
        'Minimum temperature cannot be greater than maximum temperature.'
      );
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

  // If dropdown is open then make the bottom flat
  const dropdownRadius = open ? '16px 16px 0 0' : '16px';

  return (
    <div className="vacation-page">
      <Navbar />
      <div className="vacation-page__finder">
        <div className="vacation-page__search-bar">
          {firstTime && (
            <p className="vacation-page__message">
              Search for vacation destinations that work for you!
            </p>
          )}
          <ErrorMessage errorMessage={errorMessage} />
          <MUI.Box
            sx={{
              padding: '20px',
              gap: '20px',
              borderRadius: '20px',
              background: 'white',
              maxWidth: '700px',
            }}
          >
            <MUI.Grid
              container
              spacing={2}
              alignItems="center"
              justifyContent="center"
            >
              <MUI.Grid item xs={12} sm={4}>
                <MUI.TextField
                  id="minTemp-input"
                  label="Minimum Temperature"
                  variant="outlined"
                  name="minTemp"
                  type="number"
                  value={minTemp}
                  onChange={(event) => setMinTemp(event.target.value)}
                  sx={{
                    width: '100%',
                    '& .MuiOutlinedInput-root': {
                      borderRadius: '16px',
                    },
                  }}
                />
              </MUI.Grid>
              <MUI.Grid item xs={12} sm={4}>
                <MUI.TextField
                  id="maxTemp-input"
                  label="Maximum Temperature"
                  variant="outlined"
                  name="maxTemp"
                  type="number"
                  value={maxTemp}
                  onChange={(event) => setMaxTemp(event.target.value)}
                  sx={{
                    width: '100%',
                    '& .MuiOutlinedInput-root': {
                      borderRadius: '16px',
                    },
                  }}
                />
              </MUI.Grid>
              <MUI.Grid item xs={12} sm={4}>
                <MUI.FormControl fullWidth sx={{ minWidth: 120 }}>
                  <MUI.InputLabel id="month-select-label">Month</MUI.InputLabel>
                  <MUI.Select
                    label="Month"
                    value={month}
                    onChange={(event) => setSelectedMonth(event.target.value)}
                    onOpen={() => setOpen(true)}
                    onClose={() => setOpen(false)}
                    sx={{ borderRadius: dropdownRadius }}
                    MenuProps={{
                      anchorOrigin: {
                        vertical: 'bottom',
                        horizontal: 'left',
                      },
                      transformOrigin: {
                        vertical: 'top',
                        horizontal: 'left',
                      },
                      PaperProps: {
                        style: {
                          maxHeight: '200px', // Set the maximum height for the dropdown menu
                          overflowY: 'auto', // Enable vertical scrolling
                        },
                      },
                    }}
                  >
                    {MONTHS.map((option) => (
                      <MUI.MenuItem key={option} value={option}>
                        {option}
                      </MUI.MenuItem>
                    ))}
                  </MUI.Select>
                </MUI.FormControl>
              </MUI.Grid>
              <MUI.Grid
                item
                xs={12}
                sm={4}
                sx={{ display: 'flex', justifyContent: 'center' }}
              >
                <MUI.Button
                  variant="contained"
                  onClick={() => getData(minTemp, maxTemp)}
                  sx={{
                    borderRadius: '12px',
                    textTransform: 'none',
                    fontSize: '1rem',
                    padding: '10px 30px',
                  }}
                >
                  Search
                </MUI.Button>
              </MUI.Grid>
            </MUI.Grid>
          </MUI.Box>
        </div>
        {cityData && <CountriesList locations={cityData}></CountriesList>}
      </div>
    </div>
  );
};
