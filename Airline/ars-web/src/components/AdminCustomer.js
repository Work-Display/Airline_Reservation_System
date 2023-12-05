
import React from 'react';
import axios from 'axios';
import { useState, useEffect } from 'react';
import TableRowDel from './TableRowDel';
import { TableCell } from "@mui/material";
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

function AdminCustomer() {
  // Customer
  const customerKeys =  ['id', 'first name', 'last name', 'address', 'phone no.', 'credit card no.', 'user id', 'actions']
  const [customers, setCustomers] = useState([]);
  const [customerUserId, setCustomerUserId] = useState('');

  const [firstN, setFirstN] = useState('');
  const [lastN, setLastN] = useState('');
  const [address, setAddress] = useState('');
  const [phone, setPhone] = useState('');
  const [card, setCard] = useState('');

  const [delCustomerErr, setDelCustomerErr] = useState('');
  const [addCustomerErr, setAddCustomerErr] = useState('');
  const [success, setSuccess] = useState(false);
 
  
  async function fetchCustomers (page) {
    let myResponse = '';
    await client.get('/admin/models/customer-for-admins/?page='+page)
      .then(response => {
        myResponse = response;
        console.log(response);
        return response;
      })
      .then(data => {
        if (myResponse.status === 200){
          console.log("Fetch customers data = ", data, "   |   myResponse = ", myResponse);
          let fake = data.data.results.map(item => ({ ...item, actions: null }));
          console.log("customers with actions = ", fake);
          setCustomers(fake);
        }else{
          setCustomers([]);
        }
      }).catch(error => {
        console.log(error);
      })
  }

  async function addCustomer(e) {
    e.preventDefault();
    var formData = new FormData();
    formData.append("first_name", firstN);
    formData.append("last_name", lastN);
    formData.append("address", address);
    formData.append("phone_no", phone);
    formData.append("credit_card_no", card);
    formData.append("user_id_id", customerUserId);

    await client.post("/admin/models/customer-for-admins/", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(response => {
      console.log(response);
      if (response.status === 201){
        setAddCustomerErr('');
        setFirstN(''); 
        setLastN('');  
        setAddress('');  
        setPhone('');  
        setCard('');  
        setCustomerUserId(''); 
        console.log('Setting success to true, before this it is false: ',success);
        setSuccess(true);
      }
    }).catch(error => {
      setAddCustomerErr([Object.values(error.response.data)]);
      console.log(error);
      setSuccess(false);
    }).then(() => {
      fetchCustomers(1);
    });
}

  async function deleteCustomer (customer_id) {
    let myResponse = '';
    await client.delete("/admin/models/customer-for-admins/" + customer_id + "/")
      .then(response => {
        myResponse = response;
        console.log(response);
        return response;
      })
      .then(data => {
        if (myResponse.status === 204){
          // console.log("Data = ", data, "   |   Response = ", myResponse);
          console.log("Successfully deleted a customer with id = ", customer_id)
          setDelCustomerErr('');
      }}).catch(error => {
        setDelCustomerErr([Object.values(error.response.data)]);
        console.log("Inside delCustomerErr = ", delCustomerErr);
        console.log(error);
      }).then(() => {
        fetchCustomers(1);
      });
  }

  const handleDeleteCustomerClick = (event, customer_id) => {
    event.preventDefault();
    console.log("You chose to delete customer_id = ", customer_id, typeof(customer_id));
    deleteCustomer(customer_id);
  };


  useEffect(() => {
    fetchCustomers(1);
  }, []);


  return (

    <div className='customer'>

      <div>    

        <h1 className='important'>Customers:</h1> 
        
        <div className='warning'>
          <h2>Warning: Deleting a customer will also automatically delete all their purchased tickets. {<br/>}You can't undo this so be careful!</h2>
        </div> 
        <br/><br/>    

        <div className="filters">
          <form name='search-form2'>
            <div className='center'>
              <TableCell>
              <h2>Customers Page: </h2>
              <input type="number" name="page" min="1" onChange={(e) => { fetchCustomers(e.target.value);}}/>
              <br/><br/>
              </TableCell>
            </div>
            <br/>
            <input type="reset" onClick={(e) => { fetchCustomers(1);} }/>
            <br/>
          </form>
        </div>
        
        {customers[0]? (
          <div>

            <table className="CenterTable">
                {console.log("inside return customers[0] = ", customers[0])}
                  <thead>
                    <tr>
                      {customerKeys.map((header, index) => <th key={index}>{header}</th>)}
                    </tr>
                    </thead>
                    <tbody>
                      {customers.map((data, index) => <TableRowDel key={index} data={Object.values(data)} handleDeleteClick={handleDeleteCustomerClick} />)}
                    </tbody> 
              </table>
              <br/>
          </div>
        ):(
          <div>
            <br/><br/>
            <h1>No customers were found.</h1>
            <br/><br/>
          </div>
        )}

      {console.log("Delete Customer Error =  ", delCustomerErr)}
      {delCustomerErr? (
        <div className='error'>
        <h2>Delete failed! {delCustomerErr}</h2>
        </div>
      ) : (<></>)}
      <br/><br/>
    </div>

    <div className="filters">
      <Form name='search-form2' onSubmit={e => addCustomer(e)}>

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>First Name: </Form.Label>
          <Form.Control type="text" placeholder="Enter first name..." value={firstN} onChange={e => setFirstN(e.target.value)} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>Last Name: </Form.Label>
          <Form.Control type="text" placeholder="Enter last name..." value={lastN} onChange={e => setLastN(e.target.value)} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>Address: </Form.Label>
          <Form.Control type="text" placeholder="Enter address..." value={address} onChange={e => setAddress(e.target.value)} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>Phone Number: </Form.Label>
          <Form.Control type="text" placeholder="Enter phone number..." value={phone} onChange={e => setPhone(e.target.value)} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>Credit Card Number: </Form.Label>
          <Form.Control type="text" placeholder="Enter credit card number..." value={card} onChange={e => setCard(e.target.value)} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label>User ID: </Form.Label>
          <Form.Control type="number" min="1" placeholder="Enter user id" value={customerUserId} onChange={e => setCustomerUserId(e.target.value)} />
        </Form.Group>


        <input type="reset" onClick={(e) => { setFirstN(''); setLastN('');  setAddress(''); setPhone(''); setCard('');  setCustomerUserId(''); setSuccess(false); setAddCustomerErr('');}}/>
        
        <Button variant="primary" type="submit">
          Add
        </Button>

      </Form>
    </div>

    <br/><br/>
    <br/><br/>
    {console.log("Error =  ", addCustomerErr)}
    {addCustomerErr? (
      <div className='error'>
      <h2>Customer addition failed! {addCustomerErr}</h2>
      </div>
    ) : success? (
      <div className='info'>
      <h2>Customer addition succeeded!</h2>
      </div>
    ) : (<></>)}
    <br/><br/>
    <br/><br/> 

  </div>

  );
};

  
export default AdminCustomer;