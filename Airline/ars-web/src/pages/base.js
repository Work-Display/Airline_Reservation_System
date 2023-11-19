import '../App.css';
import React from 'react';
import { useState } from 'react';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';



function Base() {
    const [registrationToggle, setRegistrationToggle] = useState(false);

    
    function update_form_btn() {
        if (registrationToggle) {
          document.getElementById("form_btn").innerHTML = "Register";
          setRegistrationToggle(false);
        } else {
          document.getElementById("form_btn").innerHTML = "Log in";
          setRegistrationToggle(true);
        }
    }
    
    
    return(
        <div className='App'>
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


            <div className='padPlaneFrame'>
                <div className='whoosh'>
                    <img className="SSSlogo-plane" src={require('../assets/SSS-logo-plane.png')} alt="logo" />  
                </div>
            </div>

            <div className='padTxtFrame'>
                <img className="SSSlogo-txt" src={require('../assets/SSS-logo-txt.png')} alt="logo" />  
            </div>

            <div className="center">
                <div className='myTxt'>
                    <h2>Welcome guest!</h2>
                </div>
            </div>
        </div>
)};
export default Base;