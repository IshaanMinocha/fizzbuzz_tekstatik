
import { SiGithub } from "react-icons/si";

import { motion } from "framer-motion";
import { twMerge } from "tailwind-merge";

const SignIn = () => {
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
      <h1 className="text-2xl font-semibold">Sign in to your account</h1>
      <p className="text-zinc-400">
        Don't have an account?{" "}
        <a href="/signup" className="text-blue-400">
          Create one.
        </a>
      </p>
    </div>
  </div>
);



const Email = () => {
  return (
    <form onSubmit={(e) => e.preventDefault()}>
      <div className="mb-3">
        <label htmlFor="email-input" className="mb-1.5 block text-zinc-400">
          Email
        </label>
        <input
          id="email-input"
          type="email"
          placeholder="your.email@provider.com"
          className="w-full rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2 placeholder-zinc-500 ring-1 ring-transparent transition-shadow focus:outline-0 focus:ring-blue-700"
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
        />
      </div>
      <SplashButton type="submit" className="w-full">
        Sign in
      </SplashButton>
    </form>
  );
};



const SplashButton = ({ children, className, ...rest }) => {
  return (
    <button
      className={twMerge(
        "rounded-md bg-gradient-to-br from-indigo-600 from-40% to-indigo-400 px-4 py-2 text-lg text-zinc-50 ring-2ring-offset-2 ring-offset-zinc-950 transition-all hover:scale-[1.02] hover:ring-transparent active:scale-[0.98] ",
        className
      )}
      {...rest}
    >
      {children}
    </button>
  );
};

const BubbleButton = ({ children, className, ...rest }) => {
  return (
    <button
      className={twMerge(
        `
        relative z-0 flex items-center gap-2 overflow-hidden whitespace-nowrap rounded-md 
        border border-zinc-700 bg-gradient-to-br from-zinc-800 to-zinc-950
        px-3 py-1.5
        text-zinc-50 transition-all duration-300
        
        before:absolute before:inset-0
        before:-z-10 before:translate-y-[200%]
        before:scale-[2.5]
        before:rounded-[100%] before:bg-zinc-100
        before:transition-transform before:duration-500
        before:content-[""]

        hover:scale-105 hover:text-zinc-900
        hover:before:translate-y-[0%]
        active:scale-100`,
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



export default SignIn;