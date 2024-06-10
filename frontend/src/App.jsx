import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from "./pages/Login"
import Home from './pages/Home'
import Register from "./pages/Register"
import NotFound from './pages/NotFound'
import ProtectedRoute from './components/ProtectedRoute'

function Logout() {
  // Clear the tokens from local storage and go back to log in page
  localStorage.clear()
  return <Navigate to="/login" />
}

function RegisterAndLogout() {
  // Just in case old access tokens still in local storage clear them and then register
  localStorage.clear()
  return <Register />
}

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Home/>
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={ <Login /> } />
        <Route path="/logout" element={ <Logout /> } />
        <Route path="/register" element={ <RegisterAndLogout /> } />
        <Route path="*" element={ <NotFound/> }/>
      </Routes>
    </BrowserRouter>
  )
}

export default App