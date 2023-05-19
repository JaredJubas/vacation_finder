import React from 'react';
import { render, screen } from '@testing-library/react';
import { ErrorMessage } from './ErrorMessage';

describe('ErrorMessage', () => {
  it('should render the error message when provided', () => {
    const errorMessage = 'Something went wrong!';
    render(<ErrorMessage errorMessage={errorMessage} />);
    const errorAlert = screen.queryByText(errorMessage);
    expect(errorAlert).toBeVisible();
    expect(errorAlert).toHaveClass('MuiAlert-message');
  });

  it('should not render anything when no error message is provided', () => {
    render(<ErrorMessage errorMessage={null} />);
    const errorAlert = screen.queryByText(/.+/); // Matches any text
    expect(errorAlert).not.toBeInTheDocument();
  });
});
