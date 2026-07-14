import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";

interface UserInfo {
  userId: string;
  role: string;
}

function Home() {
  const [user, setUser] = useState<UserInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchMe() {
      try {
        const data = await api.get("/auth/me");
        setUser(data.user);
      } catch {
        navigate("/login");
      } finally {
        setLoading(false);
      }
    }

    fetchMe();
  }, [navigate]);

  function handleLogout() {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    navigate("/login");
  }

  if (loading) return <div>Loading...</div>;

  return (
    <div style={{ maxWidth: 400, margin: "80px auto" }}>
      <h2>Welcome</h2>
      {user && (
        <>
          <p>User ID: {user.userId}</p>
          <p>Role: {user.role}</p>
        </>
      )}
      <button onClick={handleLogout}>Log out</button>
    </div>
  );
}

export default Home;