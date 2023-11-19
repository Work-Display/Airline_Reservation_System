
import React from 'react';
import axios from 'axios';
import { useState, useEffect } from 'react';
import FlightTableRowMain from '../components/FlightTableRowMain';
import { TableCell } from "@mui/material";
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';


axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});


function Flights() {
  const flightKeys = ["id", "airline company id", "origin country id", "destination country id", "departure time", "landing time", "remaining tickets", "buy ticket"]
  const [page, setPage] = useState([]);
  const [flights, setFlights] = useState([]);
  const [url, setUrl] = useState("http://127.0.0.1:8000/api/models/flight-for-all/?page=1");
  const [id, setID] = useState(1);

  const [airline, setAirline] = useState('');
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [depart, setDepart] = useState('');
  const [land, setLand] = useState('');
  const [ticket, setTicket] = useState('');

  const [showIfBuy, setShowIfBuy] = useState(false);

  
  async function fetchFlights (url) {
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
          setPage(data.results);
        }else{
          setPage([]);
        }
      }).catch(error => {
        console.log(error);
      })
  }
  
  async function fetchFlightByID (id) {

    if (id){
      let myResponse = '';
      await fetch("http://127.0.0.1:8000/api/models/flight-for-all/"+id)
        .then(response => {
          console.log(response);
          myResponse = response;
          return response.json();
        })
        .then(data => {
          if (myResponse.status === 200){
            console.log("id data = ",data);
            setPage([data]);
          }else{
            setPage([]);
          }
        }).catch(error => {
          console.log(error);
        })
    }
    else{
      fetchFlights("http://127.0.0.1:8000/api/models/flight-for-all/?page=1");
    }
  }

  function fetchParams(e) {
    e.preventDefault();
    let myResponse = '';
    var formData = new FormData();
    formData.append("origin_country_id_id", origin);
    formData.append("destination_country_id_id", destination);
    formData.append("departure_time", depart);
    formData.append("landing_time", land);
    formData.append("remaining_tickets", ticket);
    formData.append("airline_company_id_id", airline);
    
    client.post("/api/get_flights_by_parameters/", formData, {
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
        setPage(temp);
        console.log("page = ", page);
      }
    }).catch(error => {
      console.log(error);
      setPage([false]);
    });
  }

  useEffect(() => {
    if (page[0]){
      console.log("page in useEffect = ", page)
      let fake = page.map(item => ({ ...item, actions: null }));
      console.log("flights fake = ", fake);
      setFlights(fake);
    }else {
      setFlights([]);
    }
  }, [page]);


  return (
    <div className="App">

      <img className='title' src={require('../assets/Flights.png')} alt="Title" />
      <br/><br/>
      
      <div className="filters">
        <form name='search-form2'>
          <h3>TIPS: {<br/>}{<br/>}* You can't use the 'ID' and the 'Page' filters simultaneously.{<br/>}{<br/>}* The 'Available Flights Only' filter operates on the results of the 'Page'/'ID' filter.</h3>
          <br/>
          <hr className='one'/>

          <TableCell>
          <h2>Page Number: </h2>
          <input type="number" name="page" min="1" onChange={(e) => {setUrl("http://127.0.0.1:8000/api/models/flight-for-all/?page=" + e.target.value); fetchFlights("http://127.0.0.1:8000/api/models/flight-for-all/?page=" + e.target.value);}}/>
          <br/><br/>
          </TableCell>
          <TableCell>
          <h2>ID: </h2>
          <input type="number" min="1" name="id" onChange={(e) => {setID(e.target.value); fetchFlightByID(e.target.value);}}/>
          <br/><br/>
          </TableCell>    
          <TableCell>
            <h2  style={{margin: '3px'}}> &nbsp;&nbsp;Show Only Available Flights:</h2>
            <input style={{marginLeft: '43%', alignSelf:'center'}}
              type="checkbox"
              checked={showIfBuy}
              onChange={(e) => setShowIfBuy(e.target.checked)}
            />
          <br/><br/>
          </TableCell> 
          <br/>
  
          <input type="reset" onClick={(e) => {fetchFlights("http://127.0.0.1:8000/api/models/flight-for-all/?page=1"); setShowIfBuy(false);}}/>
          <br/>          
        </form>
      
      </div>
      <div> 
        {flights[0]? (
          <div>
            <table className="CenterTable">
                {console.log("inside return page[0] = ",page[0])}
                  <thead>
                    <tr>
                      {flightKeys.map((header, index) => <th key={index}>{header}</th>)}
                    </tr>
                    </thead>
                    <tbody>
                      {flights.map((data, index) => <FlightTableRowMain key={index} data={Object.values(data)} showIfBuy={showIfBuy}/>)}
                      
                    </tbody> 
              </table>
              {/* <br/><br/> */}
          </div>
          ):(
              <div>
                <br/><br/>
                <h1>No results are available. Try again with different parameters. {<br/>}( New here? Use the page or id filter to get flight results. )</h1>
                <br/><br/><br/><br/>
              </div>
          )}
      </div>

      <div className='filters'>  
        <Form name='search-form2' onSubmit={e => fetchParams(e)}>

          <hr className='min'/>
          <h2 className='notice'>ADVANCED FLIGHT SEARCH: </h2>
          <hr className='min'/>

          <Form.Group className="mb-3" controlId="formBasicUsername">
            <Form.Label>Airline Company ID: </Form.Label>
            <Form.Control type="number" min="1" placeholder="Enter airline company id" onChange={e => setAirline(e.target.value)} />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicUsername">
            <Form.Label>Origin country ID: </Form.Label>
            <Form.Control type="number" min="1" placeholder="Enter origin country id" onChange={e => setOrigin(e.target.value)} />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicUsername">
            <Form.Label>Destination country ID: </Form.Label>
            <Form.Control type="number" min="1" placeholder="Enter destination country id" onChange={e => setDestination(e.target.value)} />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicUsername">
            <Form.Label>Departure time: </Form.Label>
            <Form.Control type="datetime" placeholder="Enter departure time (format: YYYY-MM-DD hh:mm:ss)" onChange={e => setDepart(e.target.value)} />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicUsername">
            <Form.Label>Landing time: </Form.Label>
            <Form.Control type="datetime" placeholder="Enter landing time (format: YYYY-MM-DD hh:mm:ss)" onChange={e => setLand(e.target.value)} />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicUsername">
            <Form.Label>Remaining tickets: </Form.Label>
            <Form.Control type="number" min="1" max="860" placeholder="Enter remaining tickets" onChange={e => setTicket(e.target.value)} />
          </Form.Group>

          <input type="reset" onClick={(e) => {fetchFlights("http://127.0.0.1:8000/api/models/flight-for-all/?page=1"); setLand(''); setDepart(''); setAirline(''); setOrigin(''); setDestination(''); setTicket('');}}/>

          <Button variant="primary" type="submit">
            Search
          </Button>

          <br/>
          <h3>TIPS:{<br/>}Feel free to overlay these filters.{<br/>}You must use exact values to get what you want (not partial).{<br/>}In datetime especially be careful since the format and every second matters.</h3>
          <br/>

        </Form>
      </div>
      <br/><br/><br/><br/>

    </div>

  );

};

  
export default Flights;