import { motion } from "framer-motion";
import { twMerge } from "tailwind-merge";
import axios from "axios"; 
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const SignUp = () => {
  return (
    <div className="bg-zinc-950 py-20 text-zinc-200 selection:bg-zinc-600 pt-28">
      <motion.div
        initial={{
          opacity: 0,
          y: 25,
        }}
        animate={{
          opacity: 1,
          y: 0,
        }}
        transition={{
          duration: 1.25,
          ease: "easeInOut",
        }}
        className="relative z-10 mx-auto w-full max-w-xl p-4"
      >
        <Heading />
        <Email />
      </motion.div>

      <CornerGrid />
    </div>
  );
};

const Heading = () => (
  <div>
    <div className="mb-9 mt-6 space-y-1.5">
      <h1 className="text-2xl font-semibold">Register your account</h1>
      <p className="text-zinc-400">
        Already have an account?{" "}
        <a href="/signin" className="text-blue-400">
          Login
        </a>
      </p>
    </div>
  </div>
);

const Email = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate(); 

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/user/register", {
        name,
        email,
        password,
      });

      if (response.data.success) {
      
        navigate("/signin"); 
      } else {
        alert(response.data.message);
      }
    } catch (error) {
      alert("An error occurred during registration. Please try again.");
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label htmlFor="name-input" className="mb-1.5 block text-zinc-400">
          Name
        </label>
        <input
          id="name-input"
          type="text"
          placeholder="John Doe"
          className="w-full rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2 placeholder-zinc-500 ring-1 ring-transparent transition-shadow focus:outline-0 focus:ring-blue-700"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>
      <div className="mb-3">
        <label htmlFor="email-input" className="mb-1.5 block text-zinc-400">
          Email
        </label>
        <input
          id="email-input"
          type="email"
          placeholder="your.email@provider.com"
          className="w-full rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2 placeholder-zinc-500 ring-1 ring-transparent transition-shadow focus:outline-0 focus:ring-blue-700"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <div className="mb-6">
        <div className="mb-1.5 flex items-end justify-between">
          <label htmlFor="password-input" className="block text-zinc-400">
            Password
          </label>
        </div>
        <input
          id="password-input"
          type="password"
          placeholder="••••••••••••"
          className="w-full rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2 placeholder-zinc-500 ring-1 ring-transparent transition-shadow focus:outline-0 focus:ring-blue-700"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      <SplashButton type="submit" className="w-full">
        Sign Up
      </SplashButton>
    </form>
  );
};

const SplashButton = ({ children, className, ...rest }) => {
  return (
    <button
      className={twMerge(
        "rounded-md bg-gradient-to-br from-indigo-600 from-40% to-indigo-400 px-4 py-2 text-lg text-zinc-50 ring-2 ring-offset-2 ring-offset-zinc-950 transition-all hover:scale-[1.02] hover:ring-transparent active:scale-[0.98]",
        className
      )}
      {...rest}
    >
      {children}
    </button>
  );
};

const CornerGrid = () => {
  return (
    <div
      style={{
        backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32' width='32' height='32' fill='none' stroke-width='2' stroke='rgb(30 58 138 / 0.5)'%3e%3cpath d='M0 .5H31.5V32'/%3e%3c/svg%3e")`,
      }}
      className="absolute right-0 top-0 z-0 size-[50vw]"
    >
      <div
        style={{
          backgroundImage:
            "radial-gradient(100% 100% at 100% 0%, rgba(9,9,11,0), rgba(9,9,11,1))",
        }}
        className="absolute inset-0"
      />
    </div>
  );
};

export default SignUp;
