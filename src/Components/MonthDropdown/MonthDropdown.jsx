import { useState, useEffect } from 'react';
import { MONTHS } from '../../utils/months';

const Month = ({ id, name, onClick }) => {
  return (
    <div key={id} id={id} onClick={onClick}>
      {name}
    </div>
  );
};

const MonthDropdown = ({ onSelect }) => {
  const [isOpen, setIsOpen] = useState(false);

  function handleToggle() {
    setIsOpen(!isOpen);
  }

  function handleSelect(event) {
    const newValue = event.target.id;
    const newLabel = event.target.innerHTML;
    onSelect(newValue, newLabel);
    setIsOpen(false);
  }

  function handleOutsideClick(event) {
    if (!event.target.matches('.month-dropdown')) {
      setIsOpen(false);
    }
  }

  useEffect(() => {
    window.addEventListener('click', handleOutsideClick);
    return () => {
      window.removeEventListener('click', handleOutsideClick);
    };
  }, []);

  return (
    <div className="month-container">
      <div onClick={handleToggle} className="month-dropdown">
        Month
        <div className="caret">
          <div className="caret-left"></div>
          <div className="caret-right"></div>
        </div>
      </div>
      {isOpen && (
        <div className="months" required>
          {MONTHS.map((month) => (
            <Month
              key={month.id}
              id={month.id}
              name={month.name}
              onClick={handleSelect}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default MonthDropdown;
