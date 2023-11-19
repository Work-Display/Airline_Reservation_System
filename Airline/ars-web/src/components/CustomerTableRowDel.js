import React from "react";

function CustomerTableRowDel({data, handleDeleteClick}){
    return(

        <tr>
        {Object.values(data).map((value, index) => (
        index === Object.keys(data).length - 1 ? (
            <td>
                <button
                    className="careful"
                    type="button"
                    onClick={(event) => handleDeleteClick(event, data[5])}>  
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

export default CustomerTableRowDel