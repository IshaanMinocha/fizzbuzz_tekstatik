import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Header, Hero, Features, Footer, SignIn, SignUp, DashBoard } from "./Components/index";

// ProtectedRoute component
const ProtectedRoute = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const authToken = localStorage.getItem('authToken');
    setIsLoggedIn(!!authToken);
    setIsLoading(false);
  }, []);

  if (isLoading) {
    return null;  
  }

  if (!isLoggedIn) {
    return <Navigate to="/signin" />;
  }

  return children;
};

function App() {
  return (
    <>
      <BrowserRouter>
        <Header />
        <Routes>
          <Route
            path="/"
            element={
              <>
                <Hero />
                <Features />
              </>
            }
          />
          <Route 
            path="/dashboard/*" 
            element={
              <ProtectedRoute>
                <Routes>
                  <Route path="" element={<DashBoard />} />
                  <Route path="vulnerability" element={<DashBoard />} />
                  <Route path="fuzzresult" element={<DashBoard />} />
                  <Route path="resolution" element={<DashBoard />} />
                </Routes>
              </ProtectedRoute>
            } 
          />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/signup" element={<SignUp />} />
        </Routes>
        <Footer />
      </BrowserRouter>
    </>
  );
}

export default App;