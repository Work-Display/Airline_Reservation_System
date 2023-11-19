import React from "react";

function FlightSimpleTR({ data, handleEditClick, handleDeleteClick }) {
    return (
      <tr>
        {Object.values(data).map((value, index) => (
          index === 4 || index === 5 ? (
            <td key={index}>{new Date(value).toLocaleString("pt-BR")}</td>
          ) : (
            <td key={index}>{value}</td>
          )
        ))}
      </tr>
    );
  }
export default FlightSimpleTR;

