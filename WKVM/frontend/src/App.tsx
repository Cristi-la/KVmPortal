import cookie from "cookie";
import * as React from "react"
import { Link, Routes, Route } from "react-router-dom";

// import { OpenAPI } from "./api";
// import Home from "./pages/Home";

// OpenAPI.interceptors.request.use((request) => {
//   const { csrftoken } = cookie.parse(document.cookie);
//   if (request.headers && csrftoken) {
//     request.headers["X-CSRFTOKEN"] = csrftoken;
//   }
//   return request;
// });

import GeneralError from "./pages/errors/general-error";
import MaintenanceError from "./pages/errors/maintenance-error";
import NotFoundError from "./pages/errors/not-found-error";
import UnauthorisedError from "./pages/errors/unauthorised-error";
import Logout from "./pages/auth/Logout";
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import Home from "./pages/Home";
import PageTitle from './components/PageTitle';
import OutLayout from './layouts/OutLayout';

const App = () => (
  <>
    <Routes>
      <Route path='/' Component={OutLayout}>
        <Route
          path=""
          element={
            <>
              <PageTitle title="WKVM - home" />
              <Home />
            </>
          }
        />
        <Route
          path="test"
          element={
            <>
              <PageTitle title="WKVM - home" />
              <Home />
            </>
          }
        />
        <Route
          path="test2"
          element={
            <>
              <PageTitle title="WKVM - home" />
              <Home />
            </>
          }
        />
      </Route>

      <Route
        path="/login"
        element={
          <>
            <PageTitle title="WKVM - login" />
            <Login />
          </>
        }
      />
      <Route
        path="/Logout"
        element={
          <>
            <PageTitle title="WKVM - logout" />
            <Logout />
          </>
        }
      />
      <Route
        path="/register"
        element={
          <>
            <PageTitle title="WKVM - register" />
            <Register />
          </>
        }
      />
      <Route path="/503" Component={MaintenanceError} />
      <Route path="/500" Component={GeneralError} />
      <Route path="/404" Component={NotFoundError} />
      <Route path="/401" Component={UnauthorisedError} />

      <Route path="/*" Component={NotFoundError} />
    </Routes>
  </>
);

export default App;