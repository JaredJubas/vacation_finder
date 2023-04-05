import React from 'react';
import Location from './location';

function LocationList({ locations }) {
  const countries = Object.keys(locations).sort();
  return (
    <table className="ui celled striped padded table">
      <thead>
        <tr>
          <th>
            <h3 className="ui center aligned header">Country</h3>
          </th>
          <th>
            <h3 className="ui center aligned header">Number</h3>
          </th>
          <th>
            <h3 className="ui center aligned header">City</h3>
          </th>
          <th>
            <h3 className="ui center aligned header">Weather (celsius)</h3>
          </th>
        </tr>
      </thead>
      <tbody>
        {countries.map((country, index) => {
          return (
            <tr key={index}>
              <th>{country}</th>
              {<Location locations={locations[country]}></Location>}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

export default LocationList;
