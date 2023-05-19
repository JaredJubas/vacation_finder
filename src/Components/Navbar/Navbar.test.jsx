import React from 'react';
import { render, screen } from '@testing-library/react';
import { Navbar } from './Navbar';

describe('Navbar', () => {
  it('should render the Home link', () => {
    render(<Navbar />);
    const homeLink = screen.getByText('Home');
    expect(homeLink).toBeVisible();
    expect(homeLink.href).toContain('/');
  });

  it('should render the Vacation Finder link', () => {
    render(<Navbar />);
    const vacationFinderLink = screen.getByText('Vacation Finder');
    expect(vacationFinderLink).toBeVisible();
    expect(vacationFinderLink.href).toContain('/vacationFinder');
  });
});
