import { useState, useEffect } from 'react';
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

  function handleToggle(event) {
    // Prevent handleOutsideClick from being triggered
    event.stopPropagation();
    setIsOpen(!isOpen);

    const caret = document.getElementsByClassName('caret-down')[0];
    caret.classList.toggle('caret-up');

    document
      .getElementsByClassName('month-dropdown')[0]
      .classList.toggle('bottom-flat');
  }

  function handleSelect(event) {
    const newLabel = event.target.innerHTML;
    setIsOpen(false);
    setSelectedMonth(newLabel);

    const caret = document.getElementsByClassName('caret-down')[0];
    caret.classList.remove('caret-up');

    document
      .getElementsByClassName('month-dropdown')[0]
      .classList.remove('bottom-flat');

    // Call the onSelectMonth callback function with the selected month
    if (typeof onSelectMonth === 'function') {
      onSelectMonth(newLabel);
    }
  }

  function handleOutsideClick(event) {
    if (!event.target.matches('.month-dropdown')) {
      setIsOpen(false);

      const caret = document.getElementsByClassName('caret-down')[0];
      caret.classList.remove('caret-up');

      document
        .getElementsByClassName('month-dropdown')[0]
        .classList.remove('bottom-flat');
    }
  }

  useEffect(() => {
    window.addEventListener('click', handleOutsideClick);
    return () => {
      window.removeEventListener('click', handleOutsideClick);
    };
  }, []);

  return (
    <div onClick={handleToggle} className="month-container">
      <div className="month-dropdown">
        {selectedMonth ? selectedMonth : 'Month'}
        <div className="caret-down"></div>
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
