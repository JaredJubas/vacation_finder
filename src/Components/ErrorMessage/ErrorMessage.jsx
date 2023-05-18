import './ErrorMessage.css';
import { Alert } from '@mui/material';

const ErrorMessage = ({ errorMessage }) => {
  if (!errorMessage) {
    return;
  }

  return (
    <div className="error">
      <Alert severity="error">{errorMessage}</Alert>
    </div>
  );
};

export default ErrorMessage;
