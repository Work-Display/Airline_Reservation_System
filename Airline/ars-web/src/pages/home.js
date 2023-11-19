import '../App.css';
import React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useSelector ,useDispatch } from 'react-redux';
import { updateUser } from '../redux/user';


axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});


function Home() {

  const user = useSelector((state) => state.user.user);
  const [registrationToggle, setRegistrationToggle] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [thumbnail, setThumbnail] = useState('');
  const [loginErr, setLoginErr] = useState('');
  const [signupErr, setSignupErr] = useState('');
  const dispatch = useDispatch();
  const isLoggedIn = typeof user === 'object' && user !== null; 

  useEffect(() => {
    dispatch(updateUser());
  }, []);


  function update_form_btn() {
    if (registrationToggle) {
      document.getElementById("form_btn").innerHTML = "Register";
      setRegistrationToggle(false);
    } else {
      document.getElementById("form_btn").innerHTML = "Log in";
      setRegistrationToggle(true);
    }
  }

  function submitRegistration(e) {
    e.preventDefault();
    var formData = new FormData();
    formData.append("username", username);
    formData.append("email", email);
    formData.append("password", password);
    formData.append("thumbnail", thumbnail);
    
    client.post("/api/signup/", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(data => {
      setSignupErr('');
      setThumbnail('');
      setEmail('');
      submitLogin(e)
      setRegistrationToggle(false);
    }).catch(error => {
      console.log(error);
      setSignupErr([Object.values(error.response.data)]);
    });
  }
  

  function submitLogin(e) {
    e.preventDefault();
    client.post(
      "/api/login/",
      {
        username: username,
        password: password
      }
      ).then(data => {
        dispatch(updateUser());
        setLoginErr('');
        setPassword('');
      }).catch(error => {
        console.log(error);
        setLoginErr([Object.values(error.response.data)]);
        dispatch(updateUser());
        setUsername('');
        setPassword('');
      });
  }

  function submitLogout(e) {
    e.preventDefault();
    client.post(
      "/api/logout/",
      {withCredentials: true}
    ).then(function(res) {
      dispatch(updateUser());
      setRegistrationToggle(false);
      setUsername('');
    });
  }

  if (isLoggedIn === true)  {
    return (
      <html className="App"> 
        {console.log("user if logged : ", user, "    |   isLoggedIn = ", isLoggedIn)}

          <div className="UpNav">
            <Navbar bg="dark" variant="dark">
              <Container>
              <Navbar.Brand>N.V's Airline Reservation System</Navbar.Brand>
                <Navbar.Toggle />
                <Navbar.Collapse className="justify-content-end">
                  <Navbar.Text>
                    <form onSubmit={e => submitLogout(e)}>
                      <Button type="submit" variant="light">Log out</Button>
                    </form>
                  </Navbar.Text>
                </Navbar.Collapse>
              </Container>
            </Navbar>
          </div>
            

            <div className='padPlaneFrame'>
              <div className='whoosh'>
                <img className="SSSlogo-plane" src={require('../assets/SSS-logo-plane.png')} alt="logo" />  
              </div>
            </div>

            <div className='padTxtFrame'>
              <img className="SSSlogo-txt" src={require('../assets/SSS-logo-txt.png')} alt="logo" />  
            </div>

            <div className="center" style={{width:'100%'}}>
              <div className='myTxt' >
                <h2>Welcome back {user["username"]}, you're logged in now.</h2>
              </div>
            </div>
      </html>
    );
  } else {
    return (
    <html className="App"> 
      {console.log("user else logged out : ", user, "    |   isLoggedIn = ", isLoggedIn)}
      <div>

      <div className="UpNav">
        <Navbar bg="dark" variant="dark">
          <Container>
            <Navbar.Brand>N.V's Airline Reservation System</Navbar.Brand>
            <Navbar.Toggle />
            <Navbar.Collapse className="justify-content-end">
              <Navbar.Text>
                <Button id="form_btn" onClick={update_form_btn} variant="light">Register</Button>
              </Navbar.Text>
            </Navbar.Collapse>
          </Container>
        </Navbar>
      </div>

      {
        registrationToggle ? (
          <>
            <div className="center">
              <Form onSubmit={e => submitRegistration(e)}>

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
            {signupErr? (
              <div className='error'>
              <h2>Signup failed! {signupErr}</h2>
              </div>
            ) : (<></>)}
          </>        
        ) : (
          <>
            <div className="center">
              <Form onSubmit={e => submitLogin(e)}>

                <Form.Group className="mb-3" controlId="formBasicUsername">
                  <Form.Label>Username</Form.Label>
                  <Form.Control type="text" placeholder="Enter username" value={username} onChange={e => setUsername(e.target.value)} />
                </Form.Group>

                <Form.Group className="mb-3" controlId="formBasicPassword">
                  <Form.Label>Password</Form.Label>
                  <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
                </Form.Group>

                <Button variant="primary" type="submit">
                  Submit
                </Button>
              </Form>
            </div>
            <br/><br/>
            {loginErr? (
              <div className='error'>
              <h2>{loginErr}</h2>
              </div>
            ) : (<></>)}
          </>
        )
      }
      </div>
    </html>
    );
  }
  
  
  
}
export default Home;


