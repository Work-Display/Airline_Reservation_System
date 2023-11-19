import React from 'react';
import  { createRoot } from 'react-dom/client';
import './index.css';
import { Provider } from 'react-redux';
import store from '../src/redux/store.js';
import reportWebVitals from './reportWebVitals';
import {
  createBrowserRouter,
  RouterProvider,
  Outlet,
} from "react-router-dom";
import Home from "./pages/home";
import Flights from "./pages/flights";
import Airlines from './pages/airlines';
import Countries from './pages/countries';
import MyAirline from './pages/my_airline';
import MyTickets from './pages/my_tickets';
import MyAdmin from './pages/my_administration';
import BuyTicket from './pages/buy_ticket';
import Profile from './pages/my_profile';
import SideNavBar from "./components/SideNavBar";


reportWebVitals();

const AppLayout = () => (
  <>
    <SideNavBar />
    <Outlet />
    
  </>
);

const router = createBrowserRouter([
  {
    element: <AppLayout />,
    children: [
      {
        path: "/",
        element: <Home />,
      },
      {
        path: "flights",
        element: <Flights />,
      },
      {
        path: "airlines",
        element: <Airlines />,
      },
      {
        path: "countries",
        element: <Countries />,
      },
      {
        path: "my_airline",
        element: <MyAirline />,
      },
      {
        path: "my_tickets",
        element: <MyTickets />,
      },
      {
        path: "my_administration",
        element: <MyAdmin />,
      },
      {
        path: "buy_ticket/:flight_id",
        element: <BuyTicket />,
      },
      {
        path: "my_profile/",
        element: <Profile />,
      },
    ],
  },
]);


const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Provider store={store}>
        <RouterProvider router={router}>
          <AppLayout />
       </RouterProvider>
    </Provider>
  </React.StrictMode>  
);
