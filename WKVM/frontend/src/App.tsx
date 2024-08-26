import { Routes, Route } from "react-router-dom";
import GeneralError from "./pages/errors/general-error";
import MaintenanceError from "./pages/errors/maintenance-error";
import NotFoundError from "./pages/errors/not-found-error";
import UnauthorisedError from "./pages/errors/unauthorised-error";
import Logout from "./pages/auth/Logout";
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import Home from "./pages/Home";
import HypervisorsList from './pages/hypervisors/HypervisorsList';
import VmsList from './pages/vms/VmsList';
import PageTitle from './components/PageTitle';
import OutLayout from './layouts/OutLayout';


import ProtectedRoute from './utils/ProtectedRoute';



const App = () => (
  <>
    <Routes>
        <Route path=''  element={<ProtectedRoute><OutLayout /></ProtectedRoute>}>
          <Route
            path=""
            element={
              <>
                <PageTitle title="Home" />
                <Home />
              </>
            }
          />
          <Route path='hypervisor/'>
            <Route
              index
              element={
                <>
                  <PageTitle title="Hypervisors detail" />
                  DUPA
                </>
              }
            />
            <Route
              path="db"
              element={
                <>
                  <PageTitle title="Hypervisors list" />
                  <HypervisorsList />
                </>
              }
            />
          </Route>
          <Route
            path="vm"
            element={
              <>
                <PageTitle title="Vms list" />
                <VmsList />
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