import React from "react";

function CountryTableRow({data}){
    return(
        <tr>
            {data.map((value, index) => (
                
                index===1 
                // ? (<td key={index}> <img src={require('../../../web-design/upload_img/user_flags/'+value.substring(value.lastIndexOf("/") + 1))} /> </td>)
                ? (<td key={index}> <img src={"data:image/png;base64," + value}  /> </td>)
                // ? (<td key={index}> <img src={`data:image/png;base64,${value}`} alt="Flag" /> </td>)
                : (<td key={index}> {value} </td>)
            ))}
        </tr>

    )
}

export default CountryTableRow;

