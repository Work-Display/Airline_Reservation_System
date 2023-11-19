
import React from 'react';
import axios from 'axios';
import { useState, useEffect } from 'react';
import TableRowDel from '../components/TableRowDel';
import { useSelector } from 'react-redux';


axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});


function MyTickets() {
  const ticketKeys = ["id", "flight id", "customer id", "actions"]
  const [tickets, setTickets] = useState([]);
  const [delErr, setDelErr] = useState('');

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
    if (role !== "Customer") {
      setForbidden(true);
    }else {
      setForbidden(false);
    }
  }, [isLoggedIn, user]);

  
  async function fetchMyTickets () {
    let myResponse = '';
    await client.get('/api/models/ticket-for-customers/')
      .then(response => {
        myResponse = response;
        console.log(response);
        return response;
      })
      .then(data => {
        if (myResponse.status === 200){
          // console.log("Data = ", data, "   |   Response = ", myResponse);
          let temp = Object.values(data.data).map(item => item);
          console.log("tickets temp = ",temp)
          setTickets(temp);
          let fake = Object.values(data.data).map(item => ({ ...item, actions: null }));
          console.log("tickets fake =", fake);
          setTickets(fake);
        }else{
          setTickets([]);
        }
      }).catch(error => {
        console.log(error);
      })
  }

  
  async function deleteTicket (ticket_id) {
    let myResponse = '';
    await client.delete("/api/models/ticket-for-customers/" + ticket_id + "/")
      .then(response => {
        myResponse = response;
        console.log(response);
        return response;
      })
      .then(data => {
        if (myResponse.status === 204){
          // console.log("Data = ", data, "   |   Response = ", myResponse);
          console.log("Successfully deleted a ticket with id = ", ticket_id)
          setDelErr('');
          fetchMyTickets();
      }}).catch(error => {
        setDelErr([Object.values(error.response.data)]);
        console.log("Inside setDelErr = ", setDelErr);
        console.log(error);
      })
  }


  const handleDeleteTicketClick = (event, ticket_id) => {
    event.preventDefault();
    console.log("You chose to delete ticket_id = ", ticket_id, typeof(ticket_id));
    deleteTicket(ticket_id);
  };
  

  const handleBrowseMoreClick = () => {
    const url = `/flights`;
    // Use the history object to push a new URL to the browser history
    window.history.pushState(null, '', url);
    // Force a re-render to reflect the new URL
    window.dispatchEvent(new Event('popstate'));
  };


  useEffect(() => {
    fetchMyTickets();
  }, []);


  return (
    <div className="App">

      <img className='title' src={require('../assets/MyTickets.png')} alt="Title" />
      <br/><br/>
      <br/><br/>
      {forbidden ?
      ( 
        <>
          <div className='error'>
            <h2> You are forbidden from accessing this page because you are not a customer.</h2>
          </div>
        </>
      ) : (
        <>
          <div className='main'>

            <div> 
              {/* <img className='bird-hr' src={require('../assets/bird-hr.png')} alt="bird-hr" />
              <h1 className='important'>Your ticket history:</h1>  */}
              <div className='info'>
                <h3>Bought a ticket and suddenly it's no longer here?  {<br/>}This happens because most airlines delete their outdated flights, and in the rare case in which an airline deletes a flight that hasn't departed yet, you are guaranteed an automatic full refund. </h3>
                <br/>
                </div>

              {tickets[0]? (
                <div>
                  <table className="CenterTable">
                      {console.log("inside return tickets[0] = ", tickets[0])}
                        <thead>
                          <tr>
                            {ticketKeys.map((header, index) => <th key={index}>{header}</th>)}
                          </tr>
                          </thead>
                          <tbody>
                            {tickets.map((data, index) => <TableRowDel key={index} data={Object.values(data)} handleDeleteClick={handleDeleteTicketClick} />)}
                          </tbody> 
                    </table>
                    <br/><br/>
                    <br/><br/>
                </div>
                ):(
                    <div>
                      <br/><br/>
                      <h1 className='important'>You have 0 tickets.</h1> 
                      <br/><br/><br/><br/>
                      <div className='info'>
                      <h3>Want to see something here?{<br/>}Browse the flights page and buy a ticket first.</h3>
                      <br/>
                      <button type="button" className='confirm' onClick={() => handleBrowseMoreClick()}>  
                        Go To Flights 
                      </button>
                      </div>
                      <br/><br/><br/><br/>
                    </div>
                )}
                {console.log("Error =  ", delErr)}
                {delErr? (
                  <div className='error'>
                  <h2>Deletion failed! {delErr}</h2>
                  </div>
                ) : (<></>)}
                  <br/><br/>
                  <br/><br/>
            </div>

          </div>
        </>
      )}
        
    </div>

  );
};

    
export default MyTickets;