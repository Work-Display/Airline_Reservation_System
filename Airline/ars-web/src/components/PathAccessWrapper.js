import React, { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const PathAccessWrapper = ({ allowedPaths, children }) => {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    // Check if the current path is allowed
    const isPathAllowed = allowedPaths.includes(location.pathname);

    // Redirect to a different page if the path is not allowed
    if (!isPathAllowed) {
      navigate("/", { replace: true });
    }
  }, [allowedPaths, location]);

  // Render the wrapped children
  return <>{children}</>;
};

export default PathAccessWrapper;