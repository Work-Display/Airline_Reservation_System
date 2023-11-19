import React, { useState, useEffect } from "react";
import * as FaIcons from "react-icons/fa";
import * as AiIcons from "react-icons/ai";
import { Link } from "react-router-dom";
import { SidebarData } from "./SidebarData.js";
import "../App.css";
import { IconContext } from "react-icons";
import { useSelector } from 'react-redux';


function SideNavBar() {
  const [sidebar, setSidebar] = useState(false);
  const myBlue = 'linear-gradient( rgb(0, 12, 36), rgb(18, 27, 56))';
  const showSidebar = () => setSidebar(!sidebar);
  const [role, setRole] = useState('');
  const user = useSelector((state) => state.user.user);
  const isLoggedIn = typeof user === 'object' && user !== null; 
  
  useEffect(() => {
    if (isLoggedIn === true) {
      setRole(user.user_role);
    } else {
      setRole("Anonymous");
    }
  }, [user, isLoggedIn]);

  const allowedPaths = SidebarData.filter((item) => {
    if (item.path) {
      // Check if the user has access to the path based on their role and login status
      if (
        (item.userRole === role || item.userRole === "All") &&
        (item.loggedIn === isLoggedIn || !item.loggedIn)
      ) {
        return true;
      }
    }
    return false;
  }).map((item) => item.path);

  return (
    <>
      {console.log("role_name in return = ", role, "   |   user = ", user)}
      <IconContext.Provider value={{ color: "undefined" }}>
        <div className="navbar" style={{backgroundImage: myBlue}}>
          <Link to="#" className="menu-bars">
            <FaIcons.FaBars onClick={showSidebar}/>
          </Link>
        </div>
        <nav className={sidebar ? "nav-menu active" : "nav-menu"}>
          <ul className="nav-menu-items" onClick={showSidebar} >
            <li className="navbar-toggle">
              <Link to="#" className="menu-bars">
                <AiIcons.AiOutlineClose />
              </Link>
            </li>

            {SidebarData.map((item, index) => {
              if (
                allowedPaths.includes(item.path)
              ) {
                return (
                  <li key={index} className={item.cName}>
                    <Link to={item.path}>
                      {item.icon}
                      <span>{item.title}</span>
                    </Link>
                  </li>
                );
              }

              return null;
            })}
          </ul>
        </nav>
      </IconContext.Provider>
    </>
  );
}

export default SideNavBar;
