import React from "react";

const MyAirlineRWR = ({
    editFormData,
    handleEditFormChange,
    handleCancelClick,
  }) => {
    return(
        <tr>
            <td>
                Id isn't editable
            </td>
            <td>
                <input
                type="text"
                required="required"
                placeholder="Enter a name..."
                name="Name"
                value={editFormData.fullName}
                onChange={handleEditFormChange}
                ></input>
            </td>
            <td>
                <input
                type="text"
                required="required"
                placeholder="Enter an address..."
                name="Country ID"
                value={editFormData.address}
                onChange={handleEditFormChange}
                ></input>
            </td>
            <td>
                <button type="submit">Save</button>
                <button type="button" onClick={handleCancelClick}>
                Cancel
                </button>
            </td>
        </tr>
    )
}

export default MyAirlineRWR