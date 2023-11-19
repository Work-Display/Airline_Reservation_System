import React, { useState, useEffect } from 'react';
import AdminAirline from '../components/AdminAirline';
import AdminUser from '../components/AdminUser';
import AdminCustomer from '../components/AdminCustomer';
import Admin from '../components/Admin';
import { useSelector } from 'react-redux';


function MyAdmin() {
  const [selectedComponent, setSelectedComponent] = useState(null);
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
    if (role !== "Administrator") {
      setForbidden(true);
    }else {
      setForbidden(false);
    }
  }, [isLoggedIn, user]);

  
  useEffect(() => {
    // Retrieve the selected value from localStorage on component mount
    const savedValue = localStorage.getItem('selectedValue');
    if (savedValue) {
      handleComponentChange({ target: { value: savedValue } });
    }
  }, []);


  const handleComponentChange = (event) => {
    const selectedValue = event.target.value;

    switch (selectedValue) {
      case 'airline':
        setSelectedComponent(() => <AdminAirline />);
        break;
      case 'user':
        setSelectedComponent(() => <AdminUser />);
        break;
      case 'customer':
        setSelectedComponent(() => <AdminCustomer />);
        break;
      case 'admin':
      setSelectedComponent(() => <Admin />);
      break;
      default:
        setSelectedComponent(null);
        break;
    }

    // Save the selected value to localStorage
    localStorage.setItem('selectedValue', selectedValue);
  };

  return (
    <div className="App">
      <img className='title' src={require('../assets/Admin.png')} alt="Title" />
      <br/><br/>

      {forbidden ?
      (
        <>
          <div className='error'>
            <h2> You are forbidden from accessing this page because you are not an administrator.</h2>
          </div>
        </>
      ) : (
        <>
          <h1 className='important'>Use this menu to select your desired admin service:</h1>
          <div>
            <select onChange={handleComponentChange} className='theme-blue'>
              <option value="">Select a model </option>
              <option value="user">User</option>
              <option value="customer">Customer</option>
              <option value="airline">Airline</option>
              <option value="admin">Administrator</option>
            </select>
            <br/><br/>
            <br/><br/>
            {selectedComponent && selectedComponent}
          </div>
        </>
      )}
      
    </div>
  );
}

export default MyAdmin;