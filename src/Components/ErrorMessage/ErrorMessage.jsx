import React from 'react';
import './ErrorMessage.css';
import { Alert } from '@mui/material';

export const ErrorMessage = ({ errorMessage }) => {
  if (!errorMessage) {
    return;
  }

  return (
    <div className="error">
      <Alert severity="error">{errorMessage}</Alert>
    </div>
  );
};
