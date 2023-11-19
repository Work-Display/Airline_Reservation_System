
import React from 'react';
import axios from 'axios';
import { useState, useEffect } from 'react';
import TableRowDel from '../components/TableRowDel';
import { TableCell } from "@mui/material";
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

function AdminAirline() {
  // Airline
  const airlineKeys = ["id", "name", "country id", "actions"]
  const [airlines, setAirlines] = useState([]);
  const [airlineUserId, setAirlineUserId] = useState('');
  const [airlineName, setAirlineName] = useState('');
  const [countryId, setCountryId] = useState('');
  const [delAirlineErr, setDelAirlineErr] = useState('');
  const [addAirlineErr, setAddAirlineErr] = useState('');
  const [success, setSuccess] = useState(false);
 
  
  async function fetchAirlines (url) {
    let myResponse = '';
    await fetch(url)
      .then(response => {
        myResponse = response;
        console.log(response);
        return response.json();
      })
      .then(data => {
        if (myResponse.status === 200){
          console.log("id data = ",data);
          let fake = data.results.map(item => ({ ...item, actions: null }));
          console.log("airlines with actions = ", fake);
          setAirlines(fake);
        }else{
          setAirlines([]);
        }
      }).catch(error => {
        console.log(error);
      })
  }

  async function addAirline(e) {
    e.preventDefault();
    var formData = new FormData();
    formData.append("name", airlineName);
    formData.append("country_id_id", countryId);
    formData.append("user_id_id", airlineUserId);
    
    await client.post("/api/models/airline-for-admins/", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(response => {
      console.log(response);
      if (response.status === 201){
        setAddAirlineErr('');
        setAirlineName(''); 
        setCountryId('');  
        setAirlineUserId(''); 
        console.log('Setting success to true, before this it is: ',success);
        setSuccess(true);
      }
    }).catch(error => {
      setAddAirlineErr([Object.values(error.response.data)]);
      console.log(error);
      setSuccess(false);
    }).then(() => {
      fetchAirlines("http://127.0.0.1:8000/api/models/airline-for-all/?page=1");
    });
}

  async function deleteAirline (airline_id) {
    let myResponse = '';
    await client.delete("/api/models/airline-for-admins/" + airline_id + "/")
      .then(response => {
        myResponse = response;
        console.log(response);
        return response;
      })
      .then(data => {
        if (myResponse.status === 204){
          // console.log("Data = ", data, "   |   Response = ", myResponse);
          console.log("Successfully deleted an airline with id = ", airline_id)
          setDelAirlineErr('');
      }}).catch(error => {
        setDelAirlineErr([Object.values(error.response.data)]);
        console.log("Inside delAirlineErr = ", delAirlineErr);
        console.log(error);
      }).then(() => {
        fetchAirlines("http://127.0.0.1:8000/api/models/airline-for-all/?page=1");
      });
  }

  const handleDeleteAirlineClick = (event, airline_id) => {
    event.preventDefault();
    console.log("You chose to delete airline_id = ", airline_id, typeof(airline_id));
    deleteAirline(airline_id);
  };


  useEffect(() => {
    fetchAirlines("http://127.0.0.1:8000/api/models/airline-for-all/?page=1");
  }, []);


  return (

    <div className='airline'>

      <div>    

        <h1 className='important'>Airlines:</h1> 
        
        <div className='warning'>
          <h2>Warning: Deleting an airline will also automatically delete all of its flights and their related tickets. {<br/>}You can't undo this so be careful!</h2>
        </div> 
        <br/><br/>    

        <div className="filters">
          <form name='search-form2'>
            <div className='center'>
              <TableCell>
              <h2>Airlines Page: </h2>
              <input type="number" name="page" min="1" onChange={(e) => { fetchAirlines("http://127.0.0.1:8000/api/models/airline-for-all/?page=" + e.target.value);}}/>
              <br/><br/>
              </TableCell>
            </div>
            <br/>
            <input type="reset" onClick={(e) => {fetchAirlines("http://127.0.0.1:8000/api/models/airline-for-all/?page=1");} }/>
            <br/>
          </form>
        </div>
        
        {airlines[0]? (
          <div>
            {/* <div className='info'>
              <h2>Deleting an airline will also automatically delete all of its flights. {<br/>}You can't undo this so be careful!</h2>
            </div> */}

            <table className="CenterTable">
                {console.log("inside return airlines[0] = ", airlines[0])}
                  <thead>
                    <tr>
                      {airlineKeys.map((header, index) => <th key={index}>{header}</th>)}
                    </tr>
                    </thead>
                    <tbody>
                      {airlines.map((data, index) => <TableRowDel key={index} data={Object.values(data)} handleDeleteClick={handleDeleteAirlineClick} />)}
                    </tbody> 
              </table>
              <br/>
          </div>
        ):(
          <div>
            <br/><br/>
            <h1>No airlines are available.</h1>
            <br/><br/>
          </div>
        )}

      {console.log("Delete Airline Error =  ", delAirlineErr)}
      {delAirlineErr? (
        <div className='error'>
        <h2>Delete failed! {delAirlineErr}</h2>
        </div>
      ) : (<></>)}
      <br/><br/>
    </div>

    <div className="filters">
      <Form name='search-form2' onSubmit={e => addAirline(e)}>

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>Airline Name: </Form.Label>
          <Form.Control type="text" placeholder="Enter airline company name..." value={airlineName} onChange={e => setAirlineName(e.target.value)} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>Country ID: </Form.Label>
          <Form.Control type="number" min="1" placeholder="Enter country id" value={countryId} onChange={e => setCountryId(e.target.value)} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>User ID: </Form.Label>
          <Form.Control type="number" min="1" placeholder="Enter user id" value={airlineUserId} onChange={e => setAirlineUserId(e.target.value)} />
        </Form.Group>

        <br/><br/><br/><br/>
        <hr/><br/><br/>
        <h3>Note:{<br/>}{<br/>} * You must first register a new user and make sure that their role id is set to 2. {<br/>}* To do that you must use the register user form of THIS page (not of the Home page!).</h3>
        <br/>
        <br/><br/>
        <hr/><br/>

        <input type="reset" onClick={(e) => { setAirlineName(''); setCountryId('');  setAirlineUserId(''); setSuccess(false); setAddAirlineErr(''); }}/>
        
        <Button variant="primary" type="submit">
          Add
        </Button>

      </Form>
    </div>

    <br/><br/>
    <br/><br/>
    {console.log("Error =  ", addAirlineErr)}
    {addAirlineErr? (
      <div className='error'>
      <h2>Airline addition failed! {addAirlineErr}</h2>
      </div>
    ) : success? (
      <div className='info'>
      <h2>Airline addition succeeded!</h2>
      </div>
    ) : (<></>)}
    <br/><br/>
    <br/><br/> 

  </div>

  );
};

  
export default AdminAirline;