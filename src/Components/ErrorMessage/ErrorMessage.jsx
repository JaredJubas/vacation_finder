import './ErrorMessage.css';

const ErrorMessage = ({ errorMessage }) => {
  if (!errorMessage) {
    return;
  }

  return (
    <div className="error">
      <p className="error__message">{errorMessage}</p>
    </div>
  );
};

export default ErrorMessage;
