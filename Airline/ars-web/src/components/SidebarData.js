import React from "react";
import * as FaIcons from "react-icons/fa";
import * as AiIcons from "react-icons/ai";
import * as IoIcons from "react-icons/io";

export const SidebarData = [
  {
    title: "Home",
    path: "/",
    icon: <AiIcons.AiFillHome />,
    cName: "nav-text",
    userRole: "All", 
    loggedIn: false, 
  },
  {
    title: "Flights",
    path: "/flights",
    icon: <IoIcons.IoIosAirplane />,
    cName: "nav-text",
    userRole: "All", 
    loggedIn: false, 
  },
  {
    title: "Airlines",
    path: "/airlines",
    icon: <IoIcons.IoIosBusiness />,
    cName: "nav-text",
    userRole: "All", 
    loggedIn: false, 
  },
  {
    title: "Countries",
    path: "/countries",
    icon: <IoIcons.IoIosGlobe />,
    cName: "nav-text",
    userRole: "All", 
    loggedIn: false, 
  },
  {
    title: "My Airline",
    path: "/my_airline",
    icon: <IoIcons.IoIosJet />,
    cName: "nav-text",
    userRole: "Airline Company", 
    loggedIn: true, 
  },
  {
    title: "My Tickets",
    path: "/my_tickets",
    icon: <IoIcons.IoIosPaper />,
    cName: "nav-text",
    userRole: "Customer", 
    loggedIn: true, 
  },
  {
    title: "Administration",
    path: "/my_administration",
    icon: <IoIcons.IoMdUnlock />,
    cName: "nav-text",
    userRole: "Administrator", 
    loggedIn: true, 
  },
  {
    title: "My Profile",
    path: "/my_profile",
    icon: <IoIcons.IoIosPerson />,
    cName: "nav-text",
    userRole: "All", 
    loggedIn: true, 
  },
];