import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import axios from 'axios';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

function Profile() {
  const user = useSelector((state) => state.user.user);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('');
  const [thumbnail, setThumbnail] = useState('');
  const isLoggedIn = typeof user === 'object' && user !== null;

  useEffect(() => {
    if (isLoggedIn === true) {
      setUsername(user.username);
      setEmail(user.email);
      setRole(user.user_role);
      // setThumbnail(user.thumbnail.substring(user.thumbnail.lastIndexOf("/") + 1));
      setThumbnail(user.thumbnail);
    }
  }, [isLoggedIn]);

  if (isLoggedIn === true) {
    return (
      <div className="App">
        <img className='title' src={require('../assets/MyProfile.png')} alt="Title" />
        <br/><br/>
        {console.log("user : ", user, "    |   isLoggedIn = ", isLoggedIn,  "   |  thumbnail = ",thumbnail)}
     
        <div className="profile-frame">
          <Form name='user-profile'>
            {thumbnail && (
            // <img className='profile-pic' src={require(`../../../web-design/upload_img/user_thumbnails/${thumbnail}`)} />
            <img className='profile-pic' src={`data:image/png;base64, ${thumbnail}`} />
            )}
            <br/><br/>

            <div className='details'>
              <h2 > Username:  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; {username} </h2>
              <br/>
              <h2 > Email:  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; {email} </h2>
              <br/>
              <h2 > Role:  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; {role} </h2>
            </div>
        
          </Form>
        </div>

        <br/><br/><br/><br/><br/><br/>

      </div>
    );
  } else {
    return (
      <div className="App">

        <img className='title' src={require('../assets/MyProfile.png')} alt="Title" />
        <br/><br/>

        {console.log("user : ", user, "    |   isLoggedIn = ", isLoggedIn)}
        <br/><br/><br/><br/>
        <div className='error'>
          <h2>You are forbidden from accessing this page because you are not logged in.</h2>
        </div>
        <br/><br/><br/><br/>
        
      </div>
    );
  }
}

export default Profile;
