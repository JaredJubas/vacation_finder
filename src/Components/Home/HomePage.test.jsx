import React from 'react';
import { render, screen } from '@testing-library/react';
import { HomePage } from './HomePage';

describe('HomePage', () => {
  it('should render the Navbar component', () => {
    render(<HomePage />);
    const linkElement = screen.getByText('Home');
    expect(linkElement).toBeVisible();
  });

  it('should render the title correctly', () => {
    const { getByRole } = render(<HomePage />);
    const title = getByRole('heading', { name: 'Vacation Finder' });
    expect(title).toBeVisible();
  });

  it('should have a link with the correct URL', () => {
    const { getByText } = render(<HomePage />);
    const link = getByText('Get started!');
    expect(link.href).toContain('/vacationFinder');
  });
});
