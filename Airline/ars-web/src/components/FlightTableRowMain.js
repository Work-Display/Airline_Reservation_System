import React from "react";

function FlightTableRowMain({ data, showIfBuy }) {
  const currentTime = new Date();

  const isDepartureWithinOneHour = () => {
    const departureTime = new Date(data[4]);
    const timeDifference = departureTime.getTime() - currentTime.getTime();
    const minutesDifference = Math.floor(timeDifference / (1000 * 60));
    return minutesDifference <= 60;
  };

  const isTicketsRemainingZero = () => {
    const remainingTickets = data[6];
    return remainingTickets === 0;
  };

  const getConditionText = () => {
    let explain = ""
    if (isDepartureWithinOneHour()) {
      explain += " Departure is within an hour or already departed.";
    }
    if (isTicketsRemainingZero()) {
      explain += " No remaining tickets.";
    }
    return (
      <>
        <br />
        {'(' + explain + ')'}
      </>
    );
  };

  const canBuy = () => {
    if (isDepartureWithinOneHour() || isTicketsRemainingZero()){
      return false;
    }else {
      return true;
    }
  }

  const handleClick = (flightId) => {
    if (isDepartureWithinOneHour() || isTicketsRemainingZero()) {
      return; // Do nothing if conditions are met
    }
    const url = `/buy_ticket/${flightId}`;
    // Use the history object to push a new URL to the browser history
    window.history.pushState(null, "", url);
    // Force a re-render to reflect the new URL
    window.dispatchEvent(new Event("popstate"));
  };

  return (
    <tr>
      {showIfBuy === true
        ? (
          isDepartureWithinOneHour() || isTicketsRemainingZero()
            ? (  
              <></>
            ) : (
              data.map((value, index) => (
              <td key={index}>
                {index === 4 || index === 5 ? (
                new Date(value).toLocaleString("pt-BR")
              ) : index === Object.keys(data).length - 1 ? (
                isDepartureWithinOneHour() || isTicketsRemainingZero() ? (
                  <div className="explain">
                    <img  className="not-for-sale" src={require('../assets/forbidden.png')} alt="Not for sale: " />
                    <span className="tooltip">{getConditionText()}</span>
                  </div>
                ) : (
                  <button type="button" onClick={() => handleClick(data[0])}>
                    Buy
                  </button>
                )
              ) : (
                value
              )}
            </td>
            ))            
          )

        ) : (

          data.map((value, index) => (
            <td key={index}>
              {index === 4 || index === 5 ? (
                new Date(value).toLocaleString("pt-BR")
              ) : index === Object.keys(data).length - 1 ? (
                isDepartureWithinOneHour() || isTicketsRemainingZero() ? (
                  <div className="explain">
                    <img  className="not-for-sale" src={require('../assets/forbidden.png')} alt="Not for sale: " />
                    <span className="tooltip">{getConditionText()}</span>
                  </div>
                ) : (
                  <button type="button" onClick={() => handleClick(data[0])}>
                    Buy
                  </button>
                )
              ) : (
                value
              )}
            </td>
        ))

        )
      }
    </tr>
  );
}

export default FlightTableRowMain;