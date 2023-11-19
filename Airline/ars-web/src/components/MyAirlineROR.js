import React from "react";

function MyAirlineROR({data, handleEditClick}){
    return(
        <tr>
            {data.map((value, index) => <td key={index}>{value}</td>)}

            <td>
                <button type="button" onClick={(event) => handleEditClick(event)}>
                Edit
                </button>
            </td>

        </tr>
    )
}

export default MyAirlineROR