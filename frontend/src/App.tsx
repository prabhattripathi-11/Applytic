import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Navbar } from "./components/Navbar";
import Login from "./pages/Login";
import Home from "./pages/Home";
import "./App.css";

function AppLayout() {
  const email = localStorage.getItem("accessToken")
    ? (() => {
        try {
          const payload = JSON.parse(atob(localStorage.getItem("accessToken")!.split(".")[1]));
          return payload.email ?? null;
        } catch {
          return null;
        }
      })()
    : null;

  return (
    <>
      <Navbar userEmail={email} />
      <Home />
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;