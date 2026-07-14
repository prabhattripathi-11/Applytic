import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";

function Login() {
  const [isSignup, setIsSignup] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    try {
      if (isSignup) {
        await api.post("/auth/signup", { email, password });
        setIsSignup(false);
        setError("Account created. Please log in.");
        return;
      }

      const data = await api.post("/auth/login", { email, password });
      localStorage.setItem("accessToken", data.accessToken);
      localStorage.setItem("refreshToken", data.refreshToken);
      navigate("/");
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <div style={{ maxWidth: 320, margin: "80px auto" }}>
      <h2>{isSignup ? "Sign up" : "Log in"}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit">{isSignup ? "Sign up" : "Log in"}</button>
      </form>
      <button onClick={() => setIsSignup(!isSignup)}>
        {isSignup ? "Already have an account? Log in" : "Need an account? Sign up"}
      </button>
    </div>
  );
}

export default Login;