import { useState, useEffect, useCallback } from 'react';
import { MONTHS } from '../../utils/months';
import './MonthDropdown.css';

const Month = ({ month, onClick }) => {
  return (
    <div key={month} onClick={onClick} className="month">
      {month}
    </div>
  );
};

const MonthDropdown = ({ onSelectMonth }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedMonth, setSelectedMonth] = useState(null);

  const handleToggle = useCallback(
    (event) => {
      event.stopPropagation();
      setIsOpen(!isOpen);
    },
    [isOpen]
  );

  const handleSelect = useCallback(
    (event) => {
      event.stopPropagation();
      const newLabel = event.target.innerHTML;
      setIsOpen(false);
      setSelectedMonth(newLabel);

      onSelectMonth(newLabel);
    },
    [onSelectMonth]
  );

  const handleOutsideClick = useCallback((event) => {
    if (!event.target.matches('.month-dropdown')) {
      setIsOpen(false);
    }
  }, []);

  useEffect(() => {
    window.addEventListener('click', handleOutsideClick);
    return () => {
      window.removeEventListener('click', handleOutsideClick);
    };
  }, []);

  const dropdownClassNames = ['month-dropdown'];
  if (isOpen) {
    dropdownClassNames.push('bottom-flat');
  }

  return (
    <div onClick={handleToggle} className="month-container">
      <div className={dropdownClassNames.join(' ')}>
        {selectedMonth ? selectedMonth : 'Month'}
        <div className={`caret-down${isOpen ? ' caret-up' : ''}`}></div>
      </div>
      {isOpen && (
        <div className="months" required>
          {MONTHS.map((month) => (
            <Month key={month} month={month} onClick={handleSelect} />
          ))}
        </div>
      )}
    </div>
  );
};

export default MonthDropdown;
