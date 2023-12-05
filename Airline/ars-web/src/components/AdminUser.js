
import React from 'react';
import axios from 'axios';
import { useState, useEffect } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

function AdminUser() {
  // User
  const [userId, setUserId] = useState(0);
  const [roleId, setRoleId] = useState(0);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [thumbnail, setThumbnail] = useState('');
  const [addUserErr, setAddUserErr] = useState('');
  const [success, setSuccess] = useState(false);
 
  
  function submitSpecialRegistration(e) {
    e.preventDefault();
    var formData = new FormData();
    formData.append("username", username);
    formData.append("email", email);
    formData.append("password", password);
    formData.append("thumbnail", thumbnail);
    formData.append("user_role_id", roleId);
    
    client.post("/admin/models/user-for-admins/", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(data => {
      setAddUserErr('');
      setThumbnail('');
      setEmail('');
      setPassword('');
      setRoleId(0);
      setSuccess(true);
    }).catch(error => {
      setSuccess(false);
      console.log(error);
      setAddUserErr([Object.values(error.response.data)]);
    });
  }

  async function fetchUserID () {
    let myResponse = '';
    var formData = new FormData();
    formData.append("username", username);
    
    client.post("/admin/get-user-id-for-admins/", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(response => {
      console.log(response);
      myResponse = response;
    }).then(data => {
      setUserId(myResponse.data.id);
      setUsername('');
    }).catch(error => {
      setSuccess(false);
      console.log("Error fetching userID by username = ", username, "   | Error: ", error);
    });
  }

  useEffect(() => {
    if (success === true){
      fetchUserID();
    } else {
      setUserId(0);
    }
    
  }, [success]);


  return (

    <div className='user'>


      {/* <img className='bird-hr' src={require('../assets/bird-hr.png')} alt="bird-hr" /> */}
      <h1 className='important'>Register A User:</h1> 

      <div className="filters">
      <Form name='search-form2' onSubmit={e => submitSpecialRegistration(e)}>
      
        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>User Role ID: </Form.Label>
          <Form.Control type="number" min="1" max="3" placeholder="Enter user role id" value={roleId} onChange={e => setRoleId(e.target.value)} />
        </Form.Group>

        <br/>
        <div style={{width:'80%'}} className='info'>
          <h3> Reminder: {<br/>}Admin role id = 1 | Airline role id = 2 | Customer role id = 3</h3>
        </div>

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>Username: </Form.Label>
          <Form.Control type="text" placeholder="Enter username" value={username} onChange={e => setUsername(e.target.value)} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Email address: </Form.Label>
          <Form.Control type="email" placeholder="Enter email" value={email} onChange={e => setEmail(e.target.value)} />
          <Form.Text className="text-muted">
          </Form.Text>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password: </Form.Label>
          <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
        </Form.Group>

        <Form.Group controlId="formFile" className="mb-3">
          <Form.Label>Profile picture: </Form.Label>
          <br/>( * optional ) <br/>
          <Form.Control type="file" onChange={e => setThumbnail(e.target.files[0])} />
          <Form.Text className="text-muted">
          </Form.Text>
        </Form.Group>

        <Button variant="primary" type="submit">
          Submit
        </Button>
        </Form>
      </div>

    <br/><br/>
    <br/><br/>
    {console.log("Error =  ", addUserErr)}
    {addUserErr? (
      <div className='error'>
        <h2>User addition failed! {addUserErr}</h2>
      </div>
    ) : userId !== 0? (
      <div className='info'>
        <h2>User addition was Successful! The new user's id is: {userId}.{<br/>}Remember this ID because you'll have to use it in your Airline/Admin/Customer addition process!</h2>
      </div>
    ) : (<> </>)}
    <br/><br/><br/><br/><br/><br/>
    <br/><br/><br/><br/><br/><br/>


  </div>

  );
};

  
export default AdminUser;