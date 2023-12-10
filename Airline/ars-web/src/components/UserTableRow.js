import React from "react";

function UserTableRow({data}){
    return(
        <tr>
            {data.map((value, index) => (
                
                index===1 
                ? (<td key={index}> <img className='profile-pic' src={`data:image/png;base64, ${value}`} /> </td>)
                : (<td key={index}> {value} </td>)
            ))}
        </tr>

    )
}

export default UserTableRow;
