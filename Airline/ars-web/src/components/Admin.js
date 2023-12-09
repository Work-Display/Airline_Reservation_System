
import React from 'react';
import axios from 'axios';
import { useState, useEffect } from 'react';
import TableRowDel from './TableRowDel';
import { TableCell } from "@mui/material";
import TextField from "@mui/material/TextField";
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { useNavigate } from 'react-router-dom';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

function Admin() {
  const navigate = useNavigate();

  // Admin
  const adminKeys =  ['id', 'first name', 'last name', 'user id', 'actions']
  const [admins, setAdmins] = useState('');
  const [adminUserId, setAdminUserId] = useState('');
  const [search, setSearch] = useState('');
  const [firstN, setFirstN] = useState('');
  const [lastN, setLastN] = useState('');


  const [delAdminErr, setDelAdminErr] = useState('');
  const [addAdminErr, setAddAdminErr] = useState('');
  const [success, setSuccess] = useState(false);
 
  
  async function fetchAdmins (page) {
    let myResponse = '';
    await client.get('/admin/models/admin-for-admins/?page='+page)
      .then(response => {
        myResponse = response;
        console.log(response);
        return response;
      })
      .then(data => {
        if (myResponse.status === 200){
          console.log("Fetch admins data = ", data, "   |   myResponse = ", myResponse);
          let fake = data.data.results.map(item => ({ ...item, actions: null }));
          console.log("admins with actions = ", fake);
          setAdmins(fake);
        }else{
          setAdmins([]);
        }
      }).catch(error => {
        console.log(error);
      })
  }

  async function addAdmin(e) {
    e.preventDefault();
    var formData = new FormData();
    formData.append("first_name", firstN);
    formData.append("last_name", lastN);
    formData.append("user_id_id", adminUserId);

    await client.post("/admin/models/admin-for-admins/", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(response => {
      console.log(response);
      if (response.status === 201){
        setAddAdminErr('');
        setFirstN(''); 
        setLastN('');  
        setAdminUserId(''); 
        console.log('Setting success to true, before this it is false: ',success);
        setSuccess(true);
      }
    }).catch(error => {
      setAddAdminErr([Object.values(error.response.data)]);
      console.log(error);
      setSuccess(false);
    }).then(() => {
      fetchAdmins(1);
    });
}

  async function deleteAdmin (admin_id) {
    let myResponse = '';
    await client.delete("/admin/models/my-own-admin-delete/" + admin_id + "/")
      .then(response => {
        myResponse = response;
        console.log(response);
        return response;
      })
      .then(data => {
        if (myResponse.status === 204){
          // console.log("Data = ", data, "   |   Response = ", myResponse);
          console.log("Successfully deleted an admin with id = ", admin_id)
          setDelAdminErr('');
          navigate("/");
      }}).catch(error => {
        setDelAdminErr([Object.values(error.response.data)]);
        console.log("Inside delAdminErr = ", delAdminErr);
        console.log(error);
      }).then(() => {
        fetchAdmins(1);
      });
  }

  const handleDeleteAdminClick = (event, admin_id) => {
    event.preventDefault();
    console.log("You chose to delete admin_id = ", admin_id, typeof(admin_id));
    deleteAdmin(admin_id);
  };

  async function handleInputChange (search) { 
    let myResponse = '';
    var formData = new FormData();
    formData.append("model", "admin");
    formData.append("name", search);

    await client.post("/all/search_by_name/", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
     }})
    .then(response => {
      console.log(response);
      myResponse = response;
      return response.json;
    })
    .then(data => {
      if (myResponse.status === 200){
        console.log("search found = ", myResponse.data.found);
        const foundList = Object.values(myResponse.data.found);
        let fake = foundList.map(item => ({ ...item, actions: null }));
        setAdmins(fake);
      }else{
        setAdmins([]);
      }
    }).catch(error => {
      console.log(error);
    })
  }

  useEffect(() => {
    fetchAdmins(1);
  }, []);


  return (

    <div className='admin'>

      <div>    

        <h1 className='important'>Admins:</h1> 
        
        <div className='warning'>
          <h2>Warning: For the sake of this site's peace and stability, you can't delete any admin other than yourself. Deleting yourself will also permanently delete your user and you'll get logged out. {<br/>}You can't undo this so be careful!</h2>
        </div> 
        <br/><br/>    

        <div className="filters">
          <form name='search-form2'>
            <div className='center'>
              <TableCell>
              <h2>Admins Page: </h2>
              <input type="number" name="page" min="1" onChange={(e) => { fetchAdmins(e.target.value);}}/>
              <br/>
              </TableCell>
            </div>
            <div className="search">
              <TextField
                className="custom-textfield"
                id="outlined-basic"
                variant="outlined"
                onChange= {e => {handleInputChange(e.target.value); setSearch(e.target.value);}}
                fullWidth
                label="Search"
                placeholder='Type a name to search'
              />
            </div>
            <br/>
            <hr className='one' style={{width:'90%', borderWidth: '1.4px'}}/>
            <br/>
            <input type="reset" onClick={(e) => { fetchAdmins(1);  setSearch('');} }/>
            <br/>
          </form>
        </div>
        
        {admins[0]? (
          <div>

            <table className="CenterTable">
                {console.log("inside return admin[0] = ", admins[0])}
                  <thead>
                    <tr>
                      {adminKeys.map((header, index) => <th key={index}>{header}</th>)}
                    </tr>
                    </thead>
                    <tbody>
                      {admins.map((data, index) => <TableRowDel key={index} data={Object.values(data)} handleDeleteClick={handleDeleteAdminClick} />)}
                    </tbody> 
              </table>
              <br/>
          </div>
        ):(
          <div>
            <br/><br/>
            <h1>No admins were found.</h1>
            <br/><br/><br/><br/>
          </div>
        )}

      {console.log("Delete Admin Error =  ", delAdminErr)}
      {delAdminErr? (
        <div className='error'>
        <h2>Delete failed! {delAdminErr}</h2>
        </div>
      ) : (<></>)}
      <br/><br/>
      
    </div>

    <div className="filters">
      <Form name='search-form2' onSubmit={e => addAdmin(e)}>

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>First Name: </Form.Label>
          <Form.Control type="text" placeholder="Enter first name..." value={firstN} onChange={e => setFirstN(e.target.value)} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>Last Name: </Form.Label>
          <Form.Control type="text" placeholder="Enter last name..." value={lastN} onChange={e => setLastN(e.target.value)} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>User ID: </Form.Label>
          <Form.Control type="number" min="1" placeholder="Enter user id" value={adminUserId} onChange={e => setAdminUserId(e.target.value)} />
        </Form.Group>


        <input type="reset" onClick={(e) => { setFirstN(''); setLastN('');  setAdminUserId(''); setSuccess(false); setAddAdminErr('');}}/>
        
        <Button variant="primary" type="submit">
          Add
        </Button>

      </Form>
    </div>

    <br/><br/>
    <br/><br/>
    {console.log("Error =  ", addAdminErr)}
    {addAdminErr? (
      <>
        <div className='error'>
        <h2>Admin addition failed! {addAdminErr}</h2>
        </div>
        <br/><br/><br/><br/>
      </>
      
    ) : success? (
      <>
        <div className='info'>
        <h2>Admin addition succeeded!</h2>
        </div>
        <br/><br/><br/><br/>
      </>
      
    ) : (<></>)}
    <br/><br/>
    <br/><br/> 

  </div>

  );
};

  
export default Admin;