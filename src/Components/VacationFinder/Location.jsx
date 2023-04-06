import React from 'react';

const Location = ({ locations }) => {
  const cities = locations.map(({ city }) => city).sort();
  return (
    <div>
      {cities.map((city, index) => {
        const cityLocation = locations.find(
          (location) => location.city === city
        );
        return (
          <tr key={index}>
            <td>{index + 1}</td>
            <td>{city}</td>
            <td>{cityLocation.temperature}</td>
          </tr>
        );
      })}
    </div>
  );
};

export default Location;
