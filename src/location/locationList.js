import React from 'react'

function LocationList({ location, month }) {
  return (
    <table className='ui celled striped padded table'>
      <thead>
        <tr>
        <th>
            <h3 className='ui center aligned header'>Number</h3>
          </th>
          <th>
            <h3 className='ui center aligned header'>City</h3>
          </th>
          <th>
            <h3 className='ui center aligned header'>Country</h3>
          </th>
          <th>
            <h3 className='ui center aligned header'>Weather (celsius)</h3>
          </th>
        </tr>
      </thead>
      <tbody>
        {location.map((data, index) => {
          return (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{data.city}</td>
              <td>{data.country}</td>
              <td>{data.months[month].temperature}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  )
}

export default LocationList