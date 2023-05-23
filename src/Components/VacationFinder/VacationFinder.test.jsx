import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import axios from 'axios';
import { VacationFinder } from './VacationFinder';

jest.mock('axios');

describe('VacationFinder', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should display error message when not all search fields are not filled', () => {
    render(<VacationFinder />);

    fireEvent.click(screen.getByText('Search'));

    const errorMessage = screen.getByText('Please fill out all search fields.');
    expect(errorMessage).toBeVisible();
  });

  it('should display error message when minTemp is greater than maxTemp', () => {
    render(<VacationFinder />);

    fireEvent.change(screen.getByLabelText('Minimum Temperature'), {
      target: { value: '30' },
    });

    fireEvent.change(screen.getByLabelText('Maximum Temperature'), {
      target: { value: '20' },
    });

    const selectElement = screen.getAllByRole('button')[0];
    fireEvent.mouseDown(selectElement);

    const optionElements = screen.getAllByRole('option');
    fireEvent.click(optionElements[0], { target: { value: 'January' } });

    fireEvent.click(screen.getByText('Search'));

    const errorMessage = screen.getByText(
      'Minimum temperature cannot be greater than maximum temperature.'
    );
    expect(errorMessage).toBeVisible();
  });

  it('should display error message when API call fails', async () => {
    axios.mockRejectedValueOnce({ response: { data: {} } });

    render(<VacationFinder />);

    fireEvent.change(screen.getByLabelText('Minimum Temperature'), {
      target: { value: '20' },
    });

    fireEvent.change(screen.getByLabelText('Maximum Temperature'), {
      target: { value: '30' },
    });

    const selectElement = screen.getAllByRole('button')[0];
    fireEvent.mouseDown(selectElement);

    const optionElements = screen.getAllByRole('option');
    fireEvent.click(optionElements[0], { target: { value: 'January' } });

    fireEvent.click(screen.getByText('Search'));

    await waitFor(() => {
      const errorMessage = screen.getByText(
        'An error occurred. Please try again later.'
      );
      expect(errorMessage).toBeVisible();
    });
  });

  it('should make an API call with correct parameters and display results', async () => {
    const mockData = {
      USA: ['New York', 'Los Angeles'],
      Canada: ['Toronto', 'Vancouver'],
    };
    axios.mockResolvedValueOnce({ data: mockData });

    render(<VacationFinder />);

    fireEvent.change(screen.getByLabelText('Minimum Temperature'), {
      target: { value: '20' },
    });

    fireEvent.change(screen.getByLabelText('Maximum Temperature'), {
      target: { value: '30' },
    });

    const selectElement = screen.getAllByRole('button')[0];
    fireEvent.mouseDown(selectElement);

    const optionElements = screen.getAllByRole('option');
    fireEvent.click(optionElements[0], { target: { value: 'January' } });

    fireEvent.click(screen.getByText('Search'));

    await waitFor(() => {
      const countryUSA = screen.getByText('USA');
      const countryCanada = screen.getByText('Canada');
      expect(countryUSA).toBeVisible();
      expect(countryCanada).toBeVisible();
    });
  });
});
