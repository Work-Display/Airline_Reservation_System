import React from "react";

function FlightTableRow({ data, handleEditClick, handleDeleteClick }) {
    return (
      <tr>
        {Object.values(data).map((value, index) => (
          index === 4 || index === 5 ? (
            <td key={index}>{new Date(value).toLocaleString("pt-BR")}</td>
          ) : index === Object.keys(data).length - 1? (
            <td key={index}>
              <button
                type="button"
                // onClick={(event) => handleEditClick(event, data[Object.keys(data)[0]])}
                onClick={(event) => handleEditClick(event, data[0])}>  
                {/* {console.log("index 7, the row's id >", data[0])}  */}
                Edit
              </button>
              <button
                className="careful"
                type="button"
                // onClick={(event) => handleEditClick(event, data[Object.keys(data)[0]])}
                onClick={(event) => handleDeleteClick(event, data[0])}>  
                {/* {console.log("index 7, the row's id >", data[0])}  */}
                Delete
              </button>
            </td>
          ) : (
            <td key={index}>{value}</td>
          )
        ))}
      </tr>
    );
  }
export default FlightTableRow;

