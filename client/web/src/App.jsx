import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Header, Hero, Features, Footer, SignIn, SignUp, DashBoard } from "./Components/index";

function App() {
  return (
    <>
      <Header />
      <BrowserRouter>
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
          <Route path="/dashboard/vulnerability" element={<DashBoard />} />
          <Route path="/dashboard/fuzzresult" element={<DashBoard />} />
          <Route path="/dashboard/resolution" element={<DashBoard />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/signup" element={<SignUp />} />
        </Routes>
      </BrowserRouter>
      <Footer />
    </>
  );
}

export default App;
