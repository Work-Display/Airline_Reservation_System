
import React from 'react';
import axios from 'axios';
import { useState, useEffect } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { useSelector } from 'react-redux';
import TableRowAct from '../components/TableRowAct';
import FlightSimpleTR from '../components/FlightSimpleTR';
import { useParams } from 'react-router-dom';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});


function BuyTicket() {

  // Flight:
  const flightKeys = ["id", "airline company id", "origin country id", "destination country id", "departure time", "landing time", "remaining tickets"]
  const [flight, setFlight] = useState([]);
  const { flight_id } = useParams();
  const [flightId, setFlightId] = useState(null);
  const [error, setError] = useState(false); // for invalid flightId url error

  // User:
  const user = useSelector((state) => state.user.user);
  const [userID, setUserID] = useState(false);
  const [role, setRole] = useState('');

  // Customer:
  const customerKeys = ["id", "first name", "last name", "address", "phone number", "credit card number", "actions"]
  const [customer, setCustomer] = useState([]);
  const [isCustomer, setIsCustomer] = useState(false); // if the user's role is customer
  const [customerExists, setCustomerExists] = useState(false); // if the user has an instance in the Customers table

  const [edit, setEdit] = useState(false);
  const [addErr, setAddErr] = useState('');
  const [uptErr, setUptErr] = useState('');

  const [customerID, setCustomerID] = useState(0);
  const [firstN, setFirstN] = useState('');
  const [lastN, setLastN] = useState('');
  const [address, setAddress] = useState('');
  const [phone, setPhone] = useState('');
  const [card, setCard] = useState('');

  const [nFirstN, setNfirstN] = useState('');
  const [nLastN, setNlastN] = useState('');
  const [nAddress, setNaddress] = useState('');
  const [nPhone, setNphone] = useState('');
  const [nCard, setNcard] = useState('');

  // Ticket:
  const [ticketExists, setTicketExists] = useState(false);

  const [addTicketErr, setAddTicketErr] = useState('');

  // General:
  const [complete, setComplete] = useState(false); // marks the completion of the ticket purchase


  // ========================================================================================================================


  async function checkTicket () {
    let myResponse = '';
    await client.get("/all/models/does-flight-has-tickets/" + flight_id + "/")
      .then(response => {
        myResponse = response;
        console.log(response);
        return response;
      })
      .then(data => {
        if (myResponse.status === 200){
          setTicketExists(true);
          console.log("Ticket to flight with id = ", flight_id, " exists.")
      }}).catch(error => {
        setTicketExists(false);
        // setTicketErr([Object.values(error.response.data)]);
        console.log("CheckTicket returned an error: ", error);
      })
  }


  function addTicket(e) {
    e.preventDefault();
    let myResponse = '';
    var formData = new FormData();
    formData.append("flight_id_id", flightId);
    
    client.post("/customer/models/ticket-for-customers/", formData, {
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
        setComplete(true); // offer to browse more flights 
      }
    }).catch(error => {
      setComplete(false);
      setAddTicketErr([Object.values(error.response.data)]);
      console.log(error);
    });
  }


  async function checkCustomer () {
    let myResponse = '';
    await client.get("/customer/models/does-customer-exists/" + userID + "/")
      .then(response => {
        myResponse = response;
        console.log(response);
        return response;
      })
      .then(data => {
        if (myResponse.status === 200){
          setCustomerExists(true);
          fetchMyCustomer();
          console.log("Customer with user id = ", userID, " exists.")
      }}).catch(error => {
        setCustomerExists(false);
        // setTicketErr([Object.values(error.response.data)]);
        console.log("CheckCustomer returned an error: ", error);
      })
  }

  
  useEffect(() => {
    const flightIdFromUrl = parseInt(flight_id, 10);

    if (!isNaN(flightIdFromUrl) && flightIdFromUrl > 0) {
      setFlightId(flightIdFromUrl);
      setError(false);
    } else {
      setError(true);
    }
  }, [flight_id]);


  useEffect(() => { 
    console.log("flightId in my_tickets = ", flightId);
    fetchFlightByID();
    setComplete(false);
    if (user !== null) {
      setUserID(user.id);
      setRole(user.user_role);
      if (user.user_role === "Customer"){
        setIsCustomer(true);
      } else {
        setIsCustomer(false);
      }
    } else {
      setRole("Anonymous");
    } 
  }, [user, flightId]);


  useEffect(() => { 
    if (userID !== false) {
      if (isCustomer === true){
        checkCustomer();
      }
    }
  }, [userID]);


  useEffect(() => { 
    if (customerExists === true){
      checkTicket();
    }
  }, [customerExists]);


  function becomeCustomer(e) {
    e.preventDefault();
    let myResponse = '';
    var formData = new FormData();
    formData.append("first_name", firstN);
    formData.append("last_name", lastN);
    formData.append("address", address);
    formData.append("phone_no", phone);
    formData.append("credit_card_no", card);
    
    client.post("/customer/models/become-a-customer/", formData, {
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
        checkCustomer();
      }
    }).catch(error => {
      setAddErr([Object.values(error.response.data)]);
      console.log(error);
    });
  }
  

  async function fetchMyCustomer () {
    let myResponse = '';
    await client.get("/customer/models/my-own-customer/")
      .then(response => {
        console.log(response);
        myResponse = response;
        return response;
      })
      .then(data => {
        if (myResponse.status === 200){
          let temp = data.data.customer;
          delete temp["user_id"];
          temp["actions"] = null;          
          setCustomer([temp]);
          console.log("customer = ", temp);
          setCustomerID(temp.id);
          setFirstN(temp.first_name);
          setLastN(temp.last_name);
          setAddress(temp.address);
          setPhone(temp.phone_number);
          setCard(temp.credit_card_no);
          console.log("id = ", customerID, "   |   name = ", firstN);
        }else{
          console.log("ERROR! couldn't fetch customer : ", data);
          setCustomer([]);
          setCustomerID(0);
        }
      }).catch(error => {
        console.log("ERROR! couldn't fetch customer : ", error);
      })
 }


  function updateMyCustomer(event) {
    event.preventDefault();
    let myResponse = '';
    var formData = new FormData();
    formData.append("first_name", nFirstN);
    formData.append("last_name", nLastN);
    formData.append("address", nAddress);
    formData.append("phone_no", nPhone);
    formData.append("credit_card_no", nCard);

    console.log("In updateMyCustomer! customerID = ",customerID);
    client.patch("/customer/models/my-own-customer/"+customerID+"/", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
    ).then(response => {
      console.log("updateMyCustomer response = ", response);
      myResponse = response;
    })
    .then(data => {
      if (myResponse.status === 200){
        // fetchFlights("http://127.0.0.1:8000/airline/models/my-own-flight/?page=1"); // fetch tickets here
        setEdit(false);
        setNfirstN('');
        setNlastN('');
        setNaddress('');
        setNphone('');
        setNcard('');
        setUptErr('');
        fetchMyCustomer();
      } 
    }).catch(error => {
      setUptErr([Object.values(error.response.data)]);
      console.log("Inside setUptErr = ", setUptErr);
      console.log(error);
    });
  }


  const handleEditCustomerClick = (event) => {
    event.preventDefault();
    setEdit(true);
  };


  function handleCancelCustomerClick () {
    setEdit(false);
    setNfirstN('');
    setNlastN('');
    setNaddress('');
    setNphone('');
    setNcard('');
  };


  async function fetchFlightByID () {
    if (flightId !== null){
      let myResponse = '';
      await fetch("http://127.0.0.1:8000/all/models/flight-for-all/"+ flightId)
        .then(response => {
          console.log(response);
          myResponse = response;
          return response.json();
        })
        .then(data => {
          if (myResponse.status === 200){
            console.log("flight data = ",data);
            setFlight([data]);
          }else{
            setFlight([]);
          }
        }).catch(error => {
          console.log(error);
        })
    }
    else{
      console.log("Couldn't fetch flight because flightId is null.");
    }
  }

  const handleBrowseFlightsClick = () => {
    const url = `/flights`;
    // Use the history object to push a new URL to the browser history
    window.history.pushState(null, '', url);
    // Force a re-render to reflect the new URL
    window.dispatchEvent(new Event('popstate'));
  };

  const handleBrowseTicketsClick = () => {
    const url = `/my_tickets`;
    // Use the history object to push a new URL to the browser history
    window.history.pushState(null, '', url);
    // Force a re-render to reflect the new URL
    window.dispatchEvent(new Event('popstate'));
  };

  // ========================================================================================================================


  return (
    <div className="App">

      <img className='title' src={require('../assets/BuyTicket.png')} alt="Title" />
 
      <br/><br/>
      <br/><br/>
        <div className='main'>

          <div>
            {error ? (
              <div className='error'>
                <h2>Error: Invalid flight ID! </h2>
              </div>
            ) : (
              <>
                {/* <p>Flight ID: {flightId}</p> */}
              </>
            )}
          </div>

          <br/>
          <div>
            {isCustomer ? (
              <div>
                  {/* <h2> A customer user role: {role}. </h2> */}
                  <br/>
                  <div>

                    {customerExists ? (
                      <>
                          {/* <h2> Edit your customer details before purchase? </h2> */}
                      </>
                    ) : (
                      <> 
                        <div className='info'>
                          <h2>Info: To buy a ticket you must first fill out the customer form below to officially become a registered customer.</h2>
                        </div>
                        <br/>

                        <div className="filters">
                          <Form name='search-form2' onSubmit={e => becomeCustomer(e)}>

                            <Form.Group className="mb-3" controlId="formBasicUsername">
                              <Form.Label>First Name: </Form.Label>
                              <Form.Control type="text" placeholder="Enter your first name..." value={firstN} onChange={e => setFirstN(e.target.value)} />
                            </Form.Group>

                            <Form.Group className="mb-3" controlId="formBasicUsername">
                              <Form.Label>Last Name: </Form.Label>
                              <Form.Control type="text" placeholder="Enter your last name..." value={lastN} onChange={e => setLastN(e.target.value)} />
                            </Form.Group>

                            <Form.Group className="mb-3" controlId="formBasicUsername">
                              <Form.Label>Address: </Form.Label>
                              <Form.Control type="text" placeholder="Enter your address..." value={address} onChange={e => setAddress(e.target.value)} />
                            </Form.Group>

                            <Form.Group className="mb-3" controlId="formBasicUsername">
                              <Form.Label>Phone Number: </Form.Label>
                              <Form.Control type="text" placeholder="Enter your phone number..." value={phone} onChange={e => setPhone(e.target.value)} />
                            </Form.Group>

                            <Form.Group className="mb-3" controlId="formBasicUsername">
                              <Form.Label>Credit Card Number: </Form.Label>
                              <Form.Control type="text" placeholder="Enter your credit card number..." value={card} onChange={e => setCard(e.target.value)} />
                            </Form.Group>

                            <br/><br/><br/><br/>
                            <hr/><br/><br/>
                            <h3>Note:{<br/>}{<br/>} * You can always edit these details before making a purchase. {<br/>}{<br/>} * You can delete your purchased tickets anytime on your "My Tickets" page. And as long {<br/>}as 24 hours haven't passed since your purchase, you will automatically receive a full refund. {<br/>}( After 24 hours pass, deleting them will just remove them from your ticket history. )</h3>
                            <br/>
                            <br/><br/>
                            <hr/><br/>

                            <input type="reset" onClick={(e) => { setFirstN(''); setLastN('');  setAddress(''); setPhone(''); setCard('');}}/>
                            
                            <Button variant="primary" type="submit">
                              Submit
                            </Button>

                          </Form>
                        </div>

                        <br/><br/>
                        <br/><br/>
                        {console.log("Error =  ", addErr)}
                          {addErr? (
                            <div className='error'>
                            <h2>Submit failed! {addErr}</h2>
                            </div>
                          ) : (<></>)}
                          <br/><br/>
                          <br/><br/> 

                      </>
                    )}
                  </div>
              </div>

            ) : (
              <>
                <div className='warning'>
                  <h2>Warning: Sorry but only customers are allowed to purchase a ticket. Your user role isn't "Customer", it is: "{role}". <br/>So please register normally from the Home page first, or login from your customer user account.</h2>
                  <button className='quick-nav' type="button" onClick={() => handleBrowseFlightsClick()}>  
                    Go Back To Flights 
                  </button>
                </div>
              </>
            )}
          </div>

          {/* <br/><br/> */}
          {complete === true
          ? (
              <>
                <h1 className='important'>Your purchase was Successful! <br/></h1> 
                <br/>
        
                <h1 className='important'>To browse more flights you can return to the 'Flights' page:<br/></h1> 
                <button type="button" className='confirm' onClick={() => handleBrowseFlightsClick()}>  
                  Go To Flights 
                </button>
                <br/>

                <br/>
                <h1 className='important'>To see your tickets you can visit 'My Tickets' page:<br/></h1> 
                <button type="button" className='confirm' onClick={() => handleBrowseTicketsClick()}>  
                  Go To My Tickets 
                </button>
                <br/>
              </>
            )
          : (
              <>
                {customer[0]? (

                  <div> 
                    <h1 className='important'>You can edit your customer details here:</h1> 

                    <div>
                    <form onSubmit={e => {updateMyCustomer(e); setEdit(false);}}>
                      <table className="CenterTable">
                          {console.log("inside return customer[0] = ",customer[0])}
                          {console.log("inside return: customer id = ", customerID, "   |   name = ", firstN, "   |   phone = ", phone)}
                            <thead>
                              <tr>
                                {customerKeys.map((header, index) => <th key={index}>{header}</th>)}
                              </tr>
                              </thead>
                              <tbody>
                                {edit === false?
                                (
                                  customer.map((data, index) => <TableRowAct key={index} data={Object.values(data)} handleEditClick={handleEditCustomerClick} />)
                                ) : (
                                  <>

                                  <td>
                                      ID isn't editable: {customerID}
                                      <input type="hidden" name="id" value={customerID} ></input>
                                  </td>
                                  
                                  <td>
                                    <input
                                    type="text"
                                    required={false}
                                    placeholder="Enter your first name..."
                                    name="firstN"
                                    value={nFirstN}
                                    onChange={e => setNfirstN(e.target.value)}
                                    ></input>
                                  </td>

                                  <td>
                                    <input
                                    type="text"
                                    required={false}
                                    placeholder="Enter your last name..."
                                    name="lastN"
                                    value={nLastN}
                                    onChange={e => setNlastN(e.target.value)}
                                    ></input>
                                  </td>

                                  <td>
                                    <input
                                    type="text"
                                    required={false}
                                    placeholder="Enter your address..."
                                    name="address"
                                    value={nAddress}
                                    onChange={e => setNaddress(e.target.value)}
                                    ></input>
                                  </td>

                                  <td>
                                    <input
                                    type="text"
                                    required={false}
                                    placeholder="Enter your phone number..."
                                    name="phone"
                                    value={nPhone}
                                    onChange={e => setNphone(e.target.value)}
                                    ></input>
                                  </td>

                                  <td>
                                    <input
                                    type="text"
                                    required={false}
                                    placeholder="Enter your credit card no. ..."
                                    name="card"
                                    value={nCard}
                                    onChange={e => setNcard(e.target.value)}
                                    ></input>
                                  </td>

                                  <td>
                                      <button type="submit">Save</button>
                                      <button type="button" onClick={handleCancelCustomerClick}>
                                      Cancel
                                      </button>
                                  </td>
                                </>
                                )}
                              </tbody> 
                        </table>
                      </form>
                      {console.log("Customer update Error =  ", uptErr)}
                      {uptErr? (
                        <div className='error'>
                        <h2>Save failed! {uptErr}</h2>
                        </div>
                      ) : (<></>)}
                        <br/><br/>
                        <br/><br/>
                    </div>


                    { ticketExists === true
                    ? (
                    <div>
                      <h1 className='important'>Confirm your purchase:</h1> 

                      {flight[0]? (
                      <div>
                        <table className="CenterTable">
                            {console.log("inside return flight[0] = ",flight[0])}
                              <thead>
                                <tr>
                                  {flightKeys.map((header, index) => <th key={index}>{header}</th>)}
                                </tr>
                                </thead>
                                <tbody>
                                  {flight.map((data, index) => <FlightSimpleTR key={index} data={Object.values(data)} />)}
                                </tbody> 
                          </table>
                      </div>
                      ):(
                          <div>
                            <br/><br/>
                            <h1>Your requested flight wasn't found!</h1>
                            <br/><br/><br/><br/>
                          </div>
                      )}

                      <button type="submit" className="confirm" onClick={(event) => addTicket(event)}>  
                        Confirm
                      </button>
                      <br/><br/>

                      {console.log("addTicketErr =  ", addTicketErr)}
                        {addTicketErr? (
                          <>
                            <div className='error'>
                            <h2>Purchase failed! {addTicketErr}</h2>
                            </div>
                            <div className='info'>
                              <h2>You can always just go to another page to cancel the ticket purchasing process. {<br/>}</h2>
                              <button type="button" className='confirm' onClick={() => handleBrowseFlightsClick()}>  
                                Go To Flights 
                              </button>
                            </div>
                          </>
                        ) : (<></>)}
                        <br/><br/>
                        <br/><br/> 

                    </div>
                  )
                  : (<> </>)}

                  </div>
                  ) : (<></>)
                  }
              </>
            )
          }
          
      </div>
    </div>

  );

};

    
export default BuyTicket;