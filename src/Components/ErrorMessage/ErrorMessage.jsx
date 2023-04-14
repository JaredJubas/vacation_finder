import './ErrorMessage.css';

const ErrorMessage = ({ errorMessage }) => {
  if (!errorMessage) {
    return;
  }

  return (
    <div className="error-container">
      <p className="error-message">{errorMessage}</p>
    </div>
  );
};

export default ErrorMessage;
