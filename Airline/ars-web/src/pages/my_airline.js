
import React from 'react';
import axios from 'axios';
import { useState, useEffect } from 'react';
import MyAirlineROR from '../components/MyAirlineROR';
import { TableCell } from "@mui/material";
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { useSelector } from 'react-redux';
import FlightTableRow from '../components/FlightTableRow';


axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});


function MyAirline() {
  const airlineKeys = ["id", "name", "country id", "actions"]
  const [page, setPage] = useState([]);
  const [url, setUrl] = useState("http://127.0.0.1:8000/airline/models/my-own-flight/?page=1");
  const [id, setID] = useState(0);
  const [airline, setAirline] = useState('');
  const [country, setCountry] = useState(0);

  const [newAirline, setNewAirline] = useState('');
  const [newCountry, setNewCountry] = useState('');
  const [edit, setEdit] = useState(false);
  const [err, setErr] = useState('');

  const flightKeys = ["id", "airline company id", "origin country id", "destination country id", "departure time", "landing time", "remaining tickets", "actions"]
  const [flights, setFlights] = useState([]);
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [depart, setDepart] = useState('');
  const [land, setLand] = useState('');
  const [ticket, setTicket] = useState('');
  const [addErr, setAddErr] = useState('');

  const [editF, setEditF] = useState(false);
  const [flightID, setFlightID] = useState(0);
  const [nOrigin, setNorigin] = useState('');
  const [nDestination, setNdestination] = useState('');
  const [nDepart, setNdepart] = useState('');
  const [nLand, setNland] = useState('');
  const [nTicket, setNticket] = useState('');
  const [uptErr, setUptErr] = useState('');
  const [delErr, setDelErr] = useState('');

  const [currentPage, setCurrentPage] = useState(1);
  const flightsPerPage = 10;
  
  const totalPages = Math.ceil(flights.length / flightsPerPage);
  
  const pageNumbers = [];
  for (let i = 1; i <= totalPages; i++) {
    pageNumbers.push(i);
  }
  
  const goToPage = (pageNumber) => {
    setCurrentPage(pageNumber);
  };
  
  const indexOfLastFlight = currentPage * flightsPerPage;
  const indexOfFirstFlight = indexOfLastFlight - flightsPerPage;
  const currentFlights = flights.slice(indexOfFirstFlight, indexOfLastFlight);
  
  
  const [forbidden, setForbidden] = useState(false);
  var role = '';
  const user = useSelector((state) => state.user.user);
  const isLoggedIn = typeof user === 'object' && user !== null;

  useEffect(() => { 
    if (isLoggedIn) {
      role = user.user_role;
    } else {
      role = "Anonymous";
    }
    if (role !== "Airline Company") {
      setForbidden(true);
    }else {
      setForbidden(false);
    }
  }, [isLoggedIn, user]);
  
  async function fetchMyAirline () {
    let myResponse = '';
    await client.get("/airline/models/my-own-airline/")
      .then(response => {
        console.log(response);
        myResponse = response;
        return response;
      })
      .then(data => {
        if (myResponse.status === 200){
          let temp = data.data.airline;
          delete temp["user_id"];
          setPage([temp]);
          console.log("airline data = ", data.data.airline, "   |   page = ", page);
          setID(temp.id);
          setAirline(temp.name);
          setCountry(temp.country_id);
          console.log("id = ", id, "   |   name = ", airline, "   |   country = ", country);
        }else{
          console.log("ERROR! couldn't fetch your airline company : ", data);
          setPage([]);
          setID(0);
        }
      }).catch(error => {
        console.log("ERROR! couldn't fetch your airline company : ", error);
      })
 }
  
  const handleEditClick = (event) => {
    event.preventDefault();
    setEdit(true);
  };

  const handleEditFlightClick = (event, flight_id) => {
    event.preventDefault();
    setFlightID(flight_id); // RTS: It doesn't immediately updates the state. "It schedules the update to be processed in the next render cycle." --> :( Was stuck on this for a whole hour thinking that the state was stuck at initial value. In such cases an A.I assistant proved much more useful than searching the net myself.
    console.log("You chose to edit flight_id = ", flightID, flight_id, typeof(flight_id), typeof(flightID));
    setEditF(true);
  };

  async function deleteFlight (flight_id) {
    let myResponse = '';
    await client.delete("/airline/models/my-own-flight-delete/" + flight_id + "/")
      .then(response => {
        myResponse = response;
        console.log(response);
        return response;
      })
      .then(data => {
        if (myResponse.status === 204){
          // console.log("Data = ", data, "   |   Response = ", myResponse);
          console.log("Successfully deleted a flight with id = ", flight_id)
          setDelErr('');
          fetchFlights("http://127.0.0.1:8000/airline/models/my-own-flight/?page=1");
      }}).catch(error => {
        setDelErr([Object.values(error.response.data)]);
        console.log("Inside delErr = ", delErr);
        console.log(error);
      })
  }

  const handleDeleteFlightClick = (event, flight_id) => {
    event.preventDefault();
    console.log("You chose to delete flight_id = ", flight_id, typeof(flight_id));
    deleteFlight(flight_id);
  };


  function updateMyAirline(event) {
    event.preventDefault();
    let myResponse = '';
    var formData = new FormData();
    formData.append("country_id_id", newCountry);
    formData.append("name", newAirline);
    client.patch("/airline/models/my-own-airline/"+ id+"/", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
    ).then(response => {
      console.log(response);
      myResponse = response;
    })
    .then(data => {
      if (myResponse.status === 200){
        fetchMyAirline();
        setNewAirline('');
        setNewCountry('');
        setErr('');
      } 
    }).catch(error => {
      setErr([Object.values(error.response.data)]);
      console.log("Inside err = ", err);
      console.log(error);
    });
  }

  function handleCancelClick () {
    setEdit(false);
    setNewAirline('');
    setNewCountry('');
  };

  function handleFlightCancelClick () {
    setEditF(false);
    setNdepart('');
    setNland('');
    setNorigin('');
    setNdestination('');
    setNticket('');
    setFlightID(0);
  };


  async function fetchFlights (url) {
    let myResponse = '';
    await client.get(url)
      .then(response => {
        myResponse = response;
        console.log(response);
        return response;
      })
      .then(data => {
        if (myResponse.status === 200){
          // console.log("Data = ", data, "   |   Response = ", myResponse);
          let temp = Object.values(data.data).map(item => item);
          console.log("flights temp = ",temp)
          setFlights(temp);
          let fake = Object.values(data.data).map(item => ({ ...item, actions: null }));
          console.log("flights fake =", fake);
          setFlights(fake);
        }else{
          setFlights([]);
        }
      }).catch(error => {
        console.log(error);
      })
  }

  useEffect(() => {
    fetchMyAirline();
    fetchFlights("http://127.0.0.1:8000/airline/models/my-own-flight/?page=1");
  }, []);


  function addFlight(e) {
    e.preventDefault();
    let myResponse = '';
    var formData = new FormData();
    formData.append("origin_country_id_id", origin);
    formData.append("destination_country_id_id", destination);
    formData.append("departure_time", depart);
    formData.append("landing_time", land);
    formData.append("remaining_tickets", ticket);
    formData.append("airline_company_id_id", id);
    
    client.post("/airline/models/my-own-flight-add/", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
    ).then(response => {
      console.log(response);
      myResponse = response;
    })
    .then(data => {
      if (myResponse.status === 200){
        let temp = Object.values(myResponse.data);
        console.log("page = ", page);
        setAddErr('');
        setLand(''); 
        setDepart('');  
        setOrigin(''); 
        setDestination(''); 
        setTicket('');
        fetchFlights("http://127.0.0.1:8000/airline/models/my-own-flight/?page=1");
      }
    }).catch(error => {
      setAddErr([Object.values(error.response.data)]);
      console.log(error);
    });
  }
  
  function updateMyFlight(event) {
    event.preventDefault();
    let myResponse = '';
    var formData = new FormData();
    formData.append("origin_country_id_id", nOrigin);
    formData.append("destination_country_id_id", nDestination);
    formData.append("departure_time", nDepart);
    formData.append("landing_time", nLand);
    formData.append("remaining_tickets", nTicket);
    formData.append("airline_company_id_id", id);
    console.log("In updateMyFlight! flightID = ",flightID);
    client.patch("/airline/models/my-own-flight/"+flightID+"/", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
    ).then(response => {
      console.log("UpdateMyFlight response = ", response);
      myResponse = response;
    })
    .then(data => {
      if (myResponse.status === 200){
        fetchFlights("http://127.0.0.1:8000/airline/models/my-own-flight/?page=1");
        setEditF(false);
        setNdepart('');
        setNland('');
        setNorigin('');
        setNdestination('');
        setNticket('');
        setFlightID(0);
        setUptErr('');
      } 
    }).catch(error => {
      setUptErr([Object.values(error.response.data)]);
      console.log("Inside setUptErr = ", setUptErr);
      console.log(error);
    });
  }

  return (
    <div className="App">

      <img className='title' src={require('../assets/MyAirline.png')} alt="Title" />
      <br/><br/>
      <br/><br/>
      {forbidden ?
      ( 
        <>
          <div className='error'>
            <h2> You are forbidden from accessing this page because you are not an airline company.</h2>
          </div>
        </>
      ) : ( 
        <>
          <div className='main'>
              
            <div> 
              <h1 className='important'>Your airline company's details:</h1>

              {page[0]? (
                <div>
                <form onSubmit={e => {updateMyAirline(e); setEdit(false);}}>
                  <table className="CenterTable">
                      {console.log("inside return page[0] = ",page[0])}
                      {console.log("inside return: id = ", id, "   |   name = ", airline, "   |   country = ", country)}
                        <thead>
                          <tr>
                            {airlineKeys.map((header, index) => <th key={index}>{header}</th>)}
                          </tr>
                          </thead>
                          <tbody>
                            {edit === false?
                            (
                              page.map((data, index) => <MyAirlineROR key={index} data={Object.values(data)} handleEditClick={handleEditClick} />)
                            ) : (
                              // page.map((data, index) => <MyAirlineRWR key={index} data={Object.values(data)} handleSaveClick={handleSaveClick} handleCancelClick={handleCancelClick} editFormData={editFormData} handleEditFormChange={handleEditFormChange} />)
                              <>
                              <td>
                                  ID isn't editable
                                  <input type="hidden" name="id" value={id} ></input>
                              </td>
                              <td>
                                  <input
                                  type="text"
                                  placeholder="Enter a name..."
                                  name="name"
                                  value={newAirline}
                                  onChange={e => setNewAirline(e.target.value)}
                                  ></input>
                              </td>
                              <td>
                                  <input
                                  type="number"
                                  min={1}
                                  max={249}
                                  required={false}
                                  placeholder="Enter a country id..."
                                  name="country_id"
                                  value={newCountry}
                                  onChange={e => setNewCountry(e.target.value)}
                                  ></input>
                              </td>
                              <td>
                                  <button type="submit">Save</button>
                                  <button type="button" onClick={handleCancelClick}>
                                  Cancel
                                  </button>
                              </td>
                            </>
                            )}
                          </tbody> 
                    </table>
                  </form>
                  {console.log("Error =  ", err)}
                  {err? (
                    <div className='error'>
                    <h2>Save failed! {err}</h2>
                    </div>
                  ) : (<></>)}
                    <br/><br/>
                    <br/><br/>
                </div>
                
                ):(
                    <div>
                      <br/><br/>
                      <div className='error'>
                        <h2>Error:  {<br/>}Sorry! Looks like the admin who created your user forgot to register your airline company details. {<br/>}Contact them for help.  {<br/>}{err}</h2>
                      </div>
                    </div>
                )}

              <img className='bird-hr' src={require('../assets/bird-hr.png')} alt="bird-hr" />
              <h1 className='important'>Your Flights:</h1> 

              <div> 
                {flights[0]? (
                  <div>
                    <form onSubmit={e => {updateMyFlight(e); setEditF(false);}}>
                      <table className="CenterTable">
                          {console.log("inside return flights[0] = ",flights[0])}
                            <thead>
                              <tr>
                                {flightKeys.map((header, index) => <th key={index}>{header}</th>)}
                              </tr>
                              </thead>
                              <tbody>
                                {editF === false?
                                (
                                  // flights.map((data, index) => <FlightTableRow key={index} data={Object.values(data) } handleEditClick={handleEditFlightClick} handleDeleteClick={handleDeleteFlightClick} />)
                                  currentFlights.map((data, index) => <FlightTableRow key={index} data={Object.values(data) } handleEditClick={handleEditFlightClick} handleDeleteClick={handleDeleteFlightClick} />)

                                ) : (
                                  <>
                                  <td>
                                    ID isn't editable: {flightID}
                                    <input type="hidden" value={flightID} name="id" ></input>
                                  </td>
                                  <td>
                                    Airline ID isn't editable: {id}
                                    <input type="hidden" name="id" value={id} ></input>
                                  </td>
                                  <td>
                                    <input
                                    type="number"
                                    min={1}
                                    max={249}
                                    required={false}
                                    placeholder="Enter origin country id..."
                                    name="origin_country_id"
                                    value={nOrigin}
                                    onChange={e => setNorigin(e.target.value)}
                                    ></input>
                                  </td>
                                  <td>
                                    <input
                                    type="number"
                                    min={1}
                                    max={249}
                                    required={false}
                                    placeholder="Enter destination country id..."
                                    name="destination_country_id"
                                    value={nDestination}
                                    onChange={e => setNdestination(e.target.value)}
                                    ></input>
                                  </td>
                                  <td>
                                    <input
                                    type="datetime"
                                    required={false}
                                    placeholder="Enter departure time..."
                                    name="departure_time"
                                    value={nDepart}
                                    onChange={e => setNdepart(e.target.value)}
                                    ></input>
                                  </td>
                                  <td>
                                    <input
                                    type="datetime"
                                    required={false}
                                    placeholder="Enter landing time..."
                                    name="landing_time"
                                    value={nLand}
                                    onChange={e => setNland(e.target.value)}
                                    ></input>
                                  </td>
                                  <td>
                                    <input
                                    type="number"
                                    min={0}
                                    max={860}
                                    required={false}
                                    placeholder="Enter remaining tickets..."
                                    name="remaining_tickets"
                                    value={nTicket}
                                    onChange={e => setNticket(e.target.value)}
                                    ></input>
                                  </td>
                                  <td>
                                    <button type="submit">Update</button>
                                    <button type="button" onClick={handleFlightCancelClick}>
                                    Cancel
                                    </button>
                                  </td>
                                </>
                                )}
                              </tbody> 
                        </table>
                      </form>
                      
                      {console.log("Update Flight Error =  ", uptErr)}
                      {uptErr? (
                        <div className='error'>
                        <h2>Update failed! {uptErr}</h2>
                        </div>
                      ) : (<></>)}

                      {console.log("Delete Flight Error =  ", delErr)}
                      {delErr? (
                        <div className='error'>
                        <h2>Delete failed! {delErr}</h2>
                        </div>
                      ) : (<></>)}
                      <br/><br/>
                      <br/><br/>

                      <div className="pagination">
                        <button
                          disabled={currentPage === 1}
                          onClick={() => goToPage(currentPage - 1)}
                        >
                          {'\u003c'} Previous
                        </button>
                        
                        {[...Array(totalPages)].map((_, index) => (
                          <button
                            key={index + 1}
                            onClick={() => goToPage(index + 1)}
                            className={currentPage === index + 1 ? "active" : ""}
                          >
                            {index + 1}
                          </button>
                        ))}
                        
                        <button
                          disabled={currentPage === totalPages}
                          onClick={() => goToPage(currentPage + 1)}
                        >
                          Next {'\u003e'}
                        </button>
                      </div>
                      
                    </div>

                  ):(
                      <div>
                        <br/><br/>
                        <h1>No flights were found. {<br/>}( New here? Add flights via the form below and use the page filter to get your desired flight results. )</h1>
                        <br/><br/><br/><br/>
                      </div>
                  )}
              </div>

            <img className='bird-hr' src={require('../assets/bird-hr.png')} alt="bird-hr" />
            <h1 className='important'>Add Flight:</h1> 

            {id !== 0?
            (
              <>
                  
              <div className="filters">
                <Form name='search-form2' onSubmit={e => addFlight(e)}>

                  <Form.Group className="mb-3" controlId="formBasicUsername">
                    <Form.Label>Origin country ID: </Form.Label>
                    <Form.Control type="number" min="1" placeholder="Enter origin country id" value={origin} onChange={e => setOrigin(e.target.value)} />
                  </Form.Group>

                  <Form.Group className="mb-3" controlId="formBasicUsername">
                    <Form.Label>Destination country ID: </Form.Label>
                    <Form.Control type="number" min="1" placeholder="Enter destination country id" value={destination} onChange={e => setDestination(e.target.value)} />
                  </Form.Group>

                  <Form.Group className="mb-3" controlId="formBasicUsername">
                    <Form.Label>Departure time: </Form.Label>
                    <Form.Control type="datetime" placeholder="Enter departure time (format: YYYY-MM-DD hh:mm)" value={depart} onChange={e => setDepart(e.target.value)} />
                  </Form.Group>

                  <Form.Group className="mb-3" controlId="formBasicUsername">
                    <Form.Label>Landing time: </Form.Label>
                    <Form.Control type="datetime" placeholder="Enter landing time (format: YYYY-MM-DD hh:mm)" value={land} onChange={e => setLand(e.target.value)} />
                  </Form.Group>

                  <Form.Group className="mb-3" controlId="formBasicUsername">
                    <Form.Label>Remaining tickets: </Form.Label>
                    <Form.Control type="number" min="1" max="860" placeholder="Enter remaining tickets" value={ticket} onChange={e => setTicket(e.target.value)} />
                  </Form.Group>

                  {/* <br/>
                  <h3>TIP:{<br/>}Only one of the above filters can be active at a time.</h3>
                  <br/> */}
                
                  <input type="reset" onClick={(e) => { setLand(''); setDepart('');  setOrigin(''); setDestination(''); setTicket('');}}/>
                  
                  <Button variant="primary" type="submit">
                    Add
                  </Button>

                </Form>
              </div>
              <br/><br/>
              {console.log("Error =  ", addErr)}
                {addErr? (
                  <div className='error'>
                  <h2>Addition failed! {addErr}</h2>
                  </div>
                ) : (<></>)}
                <br/><br/>
                <br/><br/>
              </>
            ) : (<>
              <div>
                <br/><br/>
                <div className='error'>
                  <h2>Error:  {<br/>}Because the admin who created your user forgot to register your airline company details, you can't add flights yet. {<br/>}Contact them for help. </h2>
                </div>
                <br/><br/><br/><br/><br/><br/><br/><br/>
              </div>
            </>)}
              
            </div>
          </div>
        </>
      )}
        
    </div>

  );

};

  
export default MyAirline;