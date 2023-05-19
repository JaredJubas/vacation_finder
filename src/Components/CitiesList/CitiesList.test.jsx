import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { CitiesList } from './CitiesList';

describe('CitiesList', () => {
  const cities = [
    { city: 'City A', temperature: 10, rain: 5 },
    { city: 'City B', temperature: 15, rain: 8 },
    { city: 'City C', temperature: 20, rain: 3 },
  ];

  it('should render the cities list with default sorting', () => {
    render(<CitiesList cities={cities} isOpen={true} />);

    // The default is to sort city names so the tooltip will initially say Sort Descending
    const cityHeader = screen.getByTitle('Sort descending');
    const cityHeaders = screen.getAllByTitle('Sort ascending');
    const temperatureHeader = cityHeaders[0];
    const rainHeader = cityHeaders[1];

    expect(cityHeaders).toHaveLength(2);
    expect(cityHeader).toHaveTextContent('City');
    expect(temperatureHeader).toHaveTextContent('Average (°C)');
    expect(rainHeader).toHaveTextContent('Precipitation (days)');

    const cityRows = screen.getAllByTestId('city-row');
    expect(cityRows).toHaveLength(3);

    // Check city row data
    const cityRow1 = cityRows[1];
    const cityRow2 = cityRows[2];
    const cityRow3 = cityRows[3];

    expect(cityRow1).toHaveTextContent('City A');
    expect(cityRow1).toHaveTextContent('10');
    expect(cityRow1).toHaveTextContent('5');

    expect(cityRow2).toHaveTextContent('City B');
    expect(cityRow2).toHaveTextContent('15');
    expect(cityRow2).toHaveTextContent('8');

    expect(cityRow3).toHaveTextContent('City C');
    expect(cityRow3).toHaveTextContent('20');
    expect(cityRow3).toHaveTextContent('3');
  });

  it('should toggle sorting order when clicking on header', () => {
    render(<CitiesList cities={cities} isOpen={true} />);

    const cityHeader = screen.getByTitle('Sort descending');
    const cityHeaders = screen.getAllByTitle('Sort ascending');
    const temperatureHeader = cityHeaders[0];
    const rainHeader = cityHeaders[1];

    fireEvent.click(cityHeader);
    fireEvent.click(temperatureHeader);
    fireEvent.click(rainHeader);

    // Check updated sorting order
    expect(cityHeader).toHaveClass('arrows__arrow-down');
    expect(temperatureHeader).toHaveClass('arrows__arrow-down');
    expect(rainHeader).toHaveClass('arrows__arrow-down');

    const cityRows = screen.getAllByRole('row');

    // Check updated city row data after sorting
    const cityRow1 = cityRows[1];
    const cityRow2 = cityRows[2];
    const cityRow3 = cityRows[3];

    expect(cityRow1).toHaveTextContent('City C');
    expect(cityRow1).toHaveTextContent('20');
    expect(cityRow1).toHaveTextContent('3');

    expect(cityRow2).toHaveTextContent('City B');
    expect(cityRow2).toHaveTextContent('15');
    expect(cityRow2).toHaveTextContent('8');

    expect(cityRow3).toHaveTextContent('City A');
    expect(cityRow3).toHaveTextContent('10');
    expect(cityRow3).toHaveTextContent('5');
  });

  it('should not render anything when the component is closed', () => {
    render(<CitiesList cities={cities} isOpen={false} />);
    const citiesDropdown = screen.queryByTestId('cities-list');
    expect(citiesDropdown).not.toBeInTheDocument();
  });
});
