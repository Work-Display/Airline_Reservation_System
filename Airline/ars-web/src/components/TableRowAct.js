import React from "react";

function TableRowAct({data, handleEditClick}){
    return(

        <tr>
        {Object.values(data).map((value, index) => (
        index === Object.keys(data).length - 1 ? (
            <td>
                <button
                    type="button"
                    onClick={(event) => handleEditClick(event, data[0])}>  
                    Edit
                </button>
            </td>
        ) : (
            <td key={index}>{value}</td>
        )
        ))}
        </tr>


    )
}

export default TableRowAct