
import React from 'react';
import axios from 'axios';
import { useState, useEffect } from 'react';
import CountryTableRow from '../components/CountryTableRow';
import { TableCell } from "@mui/material";

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;


function Countries() {
  const [page, setPage] = useState([]);
  const [url, setUrl] = useState("http://127.0.0.1:8000/api/models/country-for-all/?page=1");
  const [id, setID] = useState(1);
  const [pageNum, setPageNum] = useState(1);

  async function fetchCountries (url) {
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
  
  async function fetchCountryByID (id) {

    if (id){
      let myResponse = '';
    await fetch("http://127.0.0.1:8000/api/models/country-for-all/"+id)
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
      fetchCountries("http://127.0.0.1:8000/api/models/country-for-all/?page=1");
    }
  }

  return (
    <div className="App">

      <img className='title' src={require('../assets/Countries.png')} alt="Title" />
      <br/><br/>
      
      <div className="filters">
        <form name='search-form'>
          <h3>TIPS:{<br/>}Only one of the filters below can be active at a time.{<br/>}There are 25 pages of countries available,{<br/>}and 249 countries in total.</h3>
          <br/>
          <hr className='one' style={{width:'56%'}}/>
          <div className='center'>
            <TableCell>
            <h2>Page Number: </h2>
            <input type="number" name="page" min="1" max="25" onChange={(e) => {setUrl("http://127.0.0.1:8000/api/models/country-for-all/?page=" + e.target.value); fetchCountries("http://127.0.0.1:8000/api/models/country-for-all/?page=" + e.target.value);}}/>
            <br/><br/>
            </TableCell>
            <TableCell>
            <h2>ID: </h2>
            <input type="number" min="1" max="249" name="id" onChange={(e) => {setID(e.target.value); fetchCountryByID(e.target.value);}}/>
            <br/><br/>
            </TableCell>
          </div>
          
          <br/>
          <input type="reset" onClick={(e) => {fetchCountries("http://127.0.0.1:8000/api/models/country-for-all/?page=1");}}/>
          <br/>          
        </form>
      </div>
      <div> 
          {page[0]? (
            <div>
              <table className="CenterTable">
                  {console.log("page[0] = ",page[0])}
                    <thead>
                      <tr>
                        {Object.keys(page[0]).map((header, index) => <th key={index}>{header}</th>)}
                      </tr>
                      </thead>
                      <tbody>
                        {page.map((data, index) => <CountryTableRow key={index} data={Object.values(data)} />)}
                      </tbody> 
                </table>
                <br/><br/>
                <br/><br/>

            </div>
            ):(
                <div>
                  <br/><br/>
                  <h1>No results are available. Try again with different parameters. {<br/>}( New here? Use the page or id filter to get country results. )</h1>
                  <br/><br/><br/><br/>
                </div>
            )}
        </div>
    </div>

  );

};

  
export default Countries;