import React from "react";

function TableRowDel({data, handleDeleteClick}){
    return(

        <tr>
        {Object.values(data).map((value, index) => (
        index === Object.keys(data).length - 1 ? (
            <td>
                <button
                    className="careful"
                    type="button"
                    onClick={(event) => handleDeleteClick(event, data[0])}>  
                    Delete
                </button>
            </td>
        ) : (
            <td key={index}>{value}</td>
        )
        ))}
        </tr>


    )
}

export default TableRowDel