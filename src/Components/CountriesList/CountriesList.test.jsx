import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import { CountriesList } from './CountriesList';

describe('CountriesList', () => {
  const locations = {
    USA: [
      { city: 'New York', temperature: 15, rain: 5 },
      { city: 'Los Angeles', temperature: 15, rain: 5 },
    ],
    Canada: [
      { city: 'Toronto', temperature: 15, rain: 5 },
      { city: 'Vancouver', temperature: 15, rain: 5 },
    ],
  };

  it('should display the correct header when cities are found', () => {
    const { getByText } = render(<CountriesList locations={locations} />);
    const headerText = getByText(/Found the following 4 cities/);
    expect(headerText).toBeVisible();
  });

  it('should display the correct header when no cities are found', () => {
    const emptyLocations = {};
    const { getByText } = render(<CountriesList locations={emptyLocations} />);
    const headerText = getByText(/No cities found/);
    expect(headerText).toBeVisible();
  });

  it('should toggle dropdown when clicked', () => {
    const { getByText, queryByText } = render(
      <CountriesList locations={locations} />
    );
    const dropdown = getByText('USA');
    fireEvent.click(dropdown);
    expect(queryByText('New York')).toBeVisible();
    fireEvent.click(dropdown);
    expect(queryByText('New York')).not.toBeInTheDocument();
  });
});
