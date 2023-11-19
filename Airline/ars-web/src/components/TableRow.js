import React from "react";

// Won't work with images and displays datetimes in their yucky default format. So I made a custom one for each model that has image/datetime fields.
function TableRow({data}){
    return(
        <tr>
            {data.map((value, index) => <td key={index}>{value}</td>)}
        </tr>
    )
}

export default TableRow