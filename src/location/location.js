import React from 'react';

function Location(data) {
  return (
    <tr>
      <td>{data.city}</td>
      <td>{data.country}</td>
      <td>{data.months}</td>
    </tr>
  );
}

export default Location;
