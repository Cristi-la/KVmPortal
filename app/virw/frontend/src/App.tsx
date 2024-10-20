

// // const App = () => (
// //   <>
// //     <Routes>
// //         <Route path=''  element={<AuthProvider><ProtectedRoute><OutLayout /></ProtectedRoute></AuthProvider>}>
// //           <Route
// //             path=""
// //             element={
// //               <>
// //                 <PageTitle title="Home" />
// //                 <Home />
// //               </>
// //             }
// //           />
// //           <Route path='hypervisor'>
// //             <Route path=":id"
// //               element={
// //                 <>
// //                   <PageTitle title="Hypervisor details" />
// //                   <HypervisorDetails />
// //                 </>
// //               }
// //             />
// //             <Route index path="db"
// //               element={
// //                 <>
// //                   <PageTitle title="Hypervisors list" />
// //                   <HypervisorsList />
// //                 </>
// //               }
// //             />
// //             <Route path="provision"
// //               element={
// //                 <>
// //                   <PageTitle title="Hypervisors provisioning" />
// //                   <HypervisorsProvisioning />
// //                 </>
// //               }
// //             />
            
// //           </Route>

// //           <Route path='vm'>
// //             <Route
// //               path=":id"
// //               element={
// //                 <>
// //                   <PageTitle title="Hypervisor details" />
// //                   <HypervisorDetails />
// //                 </>
// //               }
// //             />
// //             <Route
// //               index
// //               path="db"
// //               element={
// //                 <>
// //                   <PageTitle title="Hypervisors list" />
// //                   <HypervisorsList />
// //                 </>
// //               }
// //             />
// //             <Route
// //               path="provision"
// //               element={
// //                 <>
// //                   <PageTitle title="Hypervisors provisioning" />
// //                   <HypervisorsProvisioning />
// //                 </>
// //               }
// //             />
            
// //           </Route>
// //       </Route>


// //       <Route
// //         path="/login"
// //         element={
// //           <>
// //             <PageTitle title="WKVM - login" />
// //             <Login />
// //           </>
// //         }
// //       />
// //       <Route
// //         path="/Logout"
// //         element={
// //           <>
// //             <PageTitle title="WKVM - logout" />
// //             <Logout />
// //           </>
// //         }
// //       />
// //       <Route
// //         path="/register"
// //         element={
// //           <>
// //             <PageTitle title="WKVM - register" />
// //             <Register />
// //           </>
// //         }
// //       />
// //       <Route path="/503" Component={MaintenanceError} />
// //       <Route path="/500" Component={GeneralError} />
// //       <Route path="/404" Component={NotFoundError} />
// //       <Route path="/401" Component={UnauthorisedError} />
// //       <Route path="/*" Component={NotFoundError} />
// //     </Routes>
// //   </>
// // );
import { useRoutes } from "react-router-dom";

import Home from "./pages/Home";
import GeneralError from "./pages/errors/general-error";
import MaintenanceError from "./pages/errors/maintenance-error";
import NotFoundError from "./pages/errors/not-found-error";
import UnauthorisedError from "./pages/errors/unauthorised-error";

// auth
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";

// hypervisors,vms
import HypervisorsList from './pages/hypervisors/HypervisorsList';
import HypervisorDetails from './pages/hypervisors/HypervisorDetails';
import HypervisorsProvisioning from './pages/hypervisors/HypervisorsProvisioning';
import VMsList from './pages/vms/VMsList';
import VMsDefine from './pages/vms/VMsDefine';
import VMDetail from './pages/vms/VMDetail';

// utils
import PageTitle from './utils/page-title';
import ProtectedRoute from './utils/ProtectedRoute';
import OutLayout from './layouts/OutLayout';


function App() {
  const routes = useRoutes([
    {
      path: '',
      element: <ProtectedRoute><OutLayout /></ProtectedRoute>,
      children: [
        {
          index: true,
          element: (
            <>
              <PageTitle title="Home" /><Home />
            </>
          ),
        },
        {
          path: 'hypervisor',
          children: [
            {
              index: true,
              element: (
                <>
                  <PageTitle title="Hypervisors list" />
                  <HypervisorsList />
                </>
              ),
            },
            {
              path: ':id',
              element: (
                <>
                  <PageTitle title="Hypervisor details" />
                  <HypervisorDetails />
                </>
              ),
            },
            {
              path: 'provision',
              element: (
                <>
                  <PageTitle title="Hypervisors provision" />
                  <HypervisorsProvisioning />
                </>
              ),
            },
          ],
        },
        {
          path: 'vm',
          children: [
            {
              index: true,
              path: 'db',
              element: (
                <>
                  <PageTitle title="VMs list" />
                  <VMsList />
                </>
              ),
            },
            {
              path: ':id',
              element: (
                <>
                  <PageTitle title="VM details" />
                  <VMDetail />
                </>
              ),
            },
            {
              path: 'define',
              element: (
                <>
                  <PageTitle title="VMs define" />
                  <VMsDefine />
                </>
              ),
            },
          ],
        },
      ], 
    },
    {
      path: 'login',
      element: (
        <>
          <PageTitle title="Login to virw" />
          <Login />
        </>
      ),
    },
    { path: "/503", element: <MaintenanceError /> },
    { path: "/500", element: <GeneralError /> },
    { path: "/404", element: <NotFoundError /> },
    { path: "/401", element: <UnauthorisedError /> },
    { path: "/*", element: <NotFoundError /> },
  ]);
  return routes;
}

export default App;