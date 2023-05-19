import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { CitiesList } from './CitiesList';

describe('CitiesList', () => {
  const cities = [
    { city: 'City A', temperature: 15, rain: 5 },
    { city: 'City B', temperature: 10, rain: 8 },
    { city: 'City C', temperature: 20, rain: 3 },
  ];

  it('should render the cities list with default sorting', () => {
    const { container } = render(<CitiesList cities={cities} isOpen={true} />);

    // The default is to sort city names so the tooltip will initially say Sort Descending
    const cityHeader = screen.getByTitle('Sort descending');
    const cityHeaders = screen.getAllByTitle('Sort ascending');
    const temperatureHeader = cityHeaders[0];
    const rainHeader = cityHeaders[1];

    expect(cityHeaders).toHaveLength(2);
    expect(cityHeader).toHaveTextContent('City');
    expect(temperatureHeader).toHaveTextContent('Average (°C)');
    expect(rainHeader).toHaveTextContent('Precipitation (days)');

    const cityRows = container.getElementsByClassName('city-row');
    expect(cityRows).toHaveLength(3);

    // Check city row data
    const cityRow1 = cityRows[0];
    const cityRow2 = cityRows[1];
    const cityRow3 = cityRows[2];

    expect(cityRow1).toHaveTextContent('City A');
    expect(cityRow1).toHaveTextContent('15');
    expect(cityRow1).toHaveTextContent('5');

    expect(cityRow2).toHaveTextContent('City B');
    expect(cityRow2).toHaveTextContent('10');
    expect(cityRow2).toHaveTextContent('8');

    expect(cityRow3).toHaveTextContent('City C');
    expect(cityRow3).toHaveTextContent('20');
    expect(cityRow3).toHaveTextContent('3');
  });

  it('should toggle city name sorting order when clicking on city header', () => {
    const { container } = render(<CitiesList cities={cities} isOpen={true} />);

    const cityHeader = screen.getByTitle('Sort descending');

    expect(cityHeader).toHaveTextContent('City');

    // Default is to sort city names in ascending order
    const cityRows = container.getElementsByClassName('city-row');
    expect(cityRows).toHaveLength(3);

    // Make city names sort in descending order
    fireEvent.click(cityHeader);

    const cityRow1 = cityRows[0];
    const cityRow2 = cityRows[1];
    const cityRow3 = cityRows[2];

    expect(cityRow1).toHaveTextContent('City C');
    expect(cityRow1).toHaveTextContent('20');
    expect(cityRow1).toHaveTextContent('3');

    expect(cityRow2).toHaveTextContent('City B');
    expect(cityRow2).toHaveTextContent('10');
    expect(cityRow2).toHaveTextContent('8');

    expect(cityRow3).toHaveTextContent('City A');
    expect(cityRow3).toHaveTextContent('15');
    expect(cityRow3).toHaveTextContent('5');
  });

  it('should toggle temperature sorting order when clicking on temperature header', () => {
    const { container } = render(<CitiesList cities={cities} isOpen={true} />);

    const cityHeaders = screen.getAllByTitle('Sort ascending');
    const temperatureHeader = cityHeaders[0];
    expect(temperatureHeader).toHaveTextContent('Average (°C)');

    const cityRows = container.getElementsByClassName('city-row');
    expect(cityRows).toHaveLength(3);

    // Make temperature sort in ascending order
    fireEvent.click(temperatureHeader);

    const cityRow1 = cityRows[0];
    const cityRow2 = cityRows[1];
    const cityRow3 = cityRows[2];

    expect(cityRow1).toHaveTextContent('City B');
    expect(cityRow1).toHaveTextContent('10');
    expect(cityRow1).toHaveTextContent('8');

    expect(cityRow2).toHaveTextContent('City A');
    expect(cityRow2).toHaveTextContent('15');
    expect(cityRow2).toHaveTextContent('5');

    expect(cityRow3).toHaveTextContent('City C');
    expect(cityRow3).toHaveTextContent('20');
    expect(cityRow3).toHaveTextContent('3');
  });

  it('should toggle rain sorting order when clicking on rain header', () => {
    const { container } = render(<CitiesList cities={cities} isOpen={true} />);

    const cityHeaders = screen.getAllByTitle('Sort ascending');
    const rainHeader = cityHeaders[1];

    expect(cityHeaders).toHaveLength(2);
    expect(rainHeader).toHaveTextContent('Precipitation (days)');

    const cityRows = container.getElementsByClassName('city-row');
    expect(cityRows).toHaveLength(3);

    // Make rain sort in ascending order
    fireEvent.click(rainHeader);

    const cityRow1 = cityRows[0];
    const cityRow2 = cityRows[1];
    const cityRow3 = cityRows[2];

    expect(cityRow1).toHaveTextContent('City C');
    expect(cityRow1).toHaveTextContent('20');
    expect(cityRow1).toHaveTextContent('3');

    expect(cityRow2).toHaveTextContent('City A');
    expect(cityRow2).toHaveTextContent('15');
    expect(cityRow2).toHaveTextContent('5');

    expect(cityRow3).toHaveTextContent('City B');
    expect(cityRow3).toHaveTextContent('10');
    expect(cityRow3).toHaveTextContent('8');
  });

  it('should not render anything when the component is closed', () => {
    render(<CitiesList cities={cities} isOpen={false} />);
    const citiesDropdown = screen.queryByTestId('cities-list');
    expect(citiesDropdown).not.toBeInTheDocument();
  });
});
