import React from 'react';
import './LocationList.css';
// import Location from './Location';

const LocationList = ({ locations }) => {
  const countries = Object.keys(locations).sort();
  return (
    <div className="locations-container">
      {countries.map((country, index) => {
        const numCities = locations[country].length;
        const numCitiesText = numCities === 1 ? 'City' : 'Cities';
        return (
          <div className="country-dropdown" key={index}>
            <p className="country">{country}</p>
            <p className="num-cities">
              {numCities} {numCitiesText}
            </p>
            <div className="caret">
              <div className="caret-left"></div>
              <div className="caret-right"></div>
            </div>
          </div>
        );
      })}
    </div>
    // <table className="ui celled striped padded table">
    //   <thead>
    //     <tr>
    //       <th>
    //         <h3 className="ui center aligned header">Country</h3>
    //       </th>
    //       <th>
    //         <h3 className="ui center aligned header">Number</h3>
    //       </th>
    //       <th>
    //         <h3 className="ui center aligned header">City</h3>
    //       </th>
    //       <th>
    //         <h3 className="ui center aligned header">Weather (celsius)</h3>
    //       </th>
    //     </tr>
    //   </thead>
    //   <tbody>
    //     {countries.map((country, index) => {
    //       return (
    //         <tr key={index}>
    //           <th>{country}</th>
    //           {<Location locations={locations[country]}></Location>}
    //         </tr>
    //       );
    //     })}
    //   </tbody>
    // </table>
  );
};

export default LocationList;
