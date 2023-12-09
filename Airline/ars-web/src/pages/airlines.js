
import React from 'react';
import axios from 'axios';
import { useState, useEffect } from 'react';
import TableRow from '../components/TableRow';
import { TableCell } from "@mui/material";
import TextField from "@mui/material/TextField";
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';


axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});


function Airlines() {
  const airlineKeys = ["id", "name", "country id"]
  const [page, setPage] = useState([]);
  const [url, setUrl] = useState("http://127.0.0.1:8000/all/models/airline-for-all/?page=1");
  const [id, setID] = useState(1);
  const [search, setSearch] = useState('');
  const [currentUser, setCurrentUser] = useState('');
  const [role, setRole] = useState('');
  const [airline, setAirline] = useState('');
  const [country, setCountry] = useState('');

  async function fetchRole(){
    let myResponse = '';
    await client.get('/user/models/my-own-user/')
      .then(response => {
        myResponse = response;
        console.log(response);
      })
      .then(data => {
        if (myResponse.status === 200){
          setRole(myResponse.data["user_role"]);
          console.log("This user's role is: ",role);
        }
        else{
          setRole("Anonymous");
          console.log("This user's role is: ",role);
        }
      }).catch(error => {
        console.log(error);
        setRole("Anonymous");
        console.log("This user's role is: ",role);
      })
  }

  useEffect(() => {
    fetchRole();
  }, []);

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
          setPage(data.results);
        }else{
          setPage([]);
        }
      }).catch(error => {
        console.log(error);
      })
  }
  
  async function fetchAirlineByID (id) {

    if (id){
      let myResponse = '';
      await fetch("http://127.0.0.1:8000/all/models/airline-for-all/"+id)
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
      fetchAirlines("http://127.0.0.1:8000/all/models/airline-for-all/?page=1");
    }
  }

  function fetchParams(e) {
    e.preventDefault();
    let myResponse = '';
    var formData = new FormData();
    formData.append("country_id_id", country);
    formData.append("name", airline);
    
    client.post("/all/get_airlines_by_parameters/", formData, {
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
        temp = temp.map(item => {
          const { user_id, ...rest } = item;
          return rest;
        });
        setPage(temp);
        console.log("page = ", page);
      }
    }).catch(error => {
      console.log(error);
      setPage([false]);
    });
  }

  async function handleInputChange (search) { 
    let myResponse = '';
    var formData = new FormData();
    formData.append("model", "airline");
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
        setPage(foundList);
      }else{
        setPage([]);
      }
    }).catch(error => {
      console.log(error);
    })
  }
  
  return (
    <div className="App">

      <img className='title' src={require('../assets/Airlines.png')} alt="Title" />
      <br/><br/>
      
      <div className="filters">
        <form name='search-form'>
          <div className='center'>
            <TableCell>
            <h2>Page Number: </h2>
            <input type="number" name="page" min="1" onChange={(e) => {setUrl("http://127.0.0.1:8000/all/models/airline-for-all/?page=" + e.target.value); fetchAirlines("http://127.0.0.1:8000/all/models/airline-for-all/?page=" + e.target.value);}}/>
            <br/><br/>
            </TableCell>
            <TableCell>
            <h2>ID: </h2>
            <input type="number" min="1" name="id" onChange={(e) => {setID(e.target.value); fetchAirlineByID(e.target.value);}}/>
            <br/><br/>
            </TableCell>
          </div>
          <br/>

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

          <br/><br/>
          <hr className='one' style={{width:'90%', borderWidth: '1.4px'}}/>
          <br/>
          <h3>TIPS:{<br/>}Only one of the above filters can be active at a time.</h3>
          <br/>
          <input type="reset" onClick={(e) => {fetchAirlines("http://127.0.0.1:8000/all/models/airline-for-all/?page=1");  setSearch('');} }/>
          <br/>          
        </form>
      
        <Form name='search-form' onSubmit={e => fetchParams(e)}>

          <Form.Group className="mb-3" controlId="formBasicUsername">
            <Form.Label>Airline name: </Form.Label>
            <Form.Control type="text" placeholder="Enter an airline company's name" onChange={e => setAirline(e.target.value)} />
          </Form.Group>
        
          <Form.Group className="mb-3" controlId="formBasicUsername">
            <Form.Label>Country ID: </Form.Label>
            <Form.Control type="number" min="1" placeholder="Enter the airline's country id" onChange={e => setCountry(e.target.value)} />
          </Form.Group>
          <br/><br/>
          <hr className='one' style={{width:'90%', borderWidth: '1.4px'}}/>
          <br/>
          <h3>TIPS:{<br/>}Feel free to overlay these filters.{<br/>}You must use exact values to get what you want (not partial).</h3>
          <br/>

          <input type="reset" onClick={(e) => {fetchAirlines("http://127.0.0.1:8000/all/models/airline-for-all/?page=1");  setCountry(''); setAirline('');}}/>
          
          <Button variant="primary" type="submit">
            Search
          </Button>

        </Form>

      </div>
      <div> 
          {page[0]? (
            <div>
              <table className="CenterTable">
                  {console.log("inside return page[0] = ",page[0])}
                    <thead>
                      <tr>
                        {airlineKeys.map((header, index) => <th key={index}>{header}</th>)}
                      </tr>
                      </thead>
                      <tbody>
                        {page.map((data, index) => <TableRow key={index} data={Object.values(data)} />)}
                      </tbody> 
                </table>
                <br/><br/>
                <br/><br/>
            </div>
            ):(
                <div>
                  <br/><br/>
                  <h1>No results are available. Try again with different parameters. {<br/>}( New here? Use the page or id filter to get airline results. )</h1>
                  <br/><br/><br/><br/>
                </div>
            )}
        </div>
    </div>

  );

};

  
export default Airlines;