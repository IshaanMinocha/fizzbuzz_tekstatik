import { useEffect, useRef, useState } from "react";
import { useAnimate, motion } from "framer-motion";
import { FiMenu, FiArrowUpRight, FiLogOut } from "react-icons/fi";
import useMeasure from "react-use-measure";

const Header = () => {
  return (
    <GlassNavigation />
  );
};

const GlassNavigation = () => {
  const [hovered, setHovered] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const [scope, animate] = useAnimate();
  const navRef = useRef(null);

  useEffect(() => {
    const authToken = localStorage.getItem('authToken');
    setIsLoggedIn(!!authToken);
  }, []);

  const handleMouseMove = ({ offsetX, offsetY, target }) => {
    // @ts-ignore
    const isNavElement = [...target.classList].includes("glass-nav");

    if (isNavElement) {
      setHovered(true);

      const top = offsetY + "px";
      const left = offsetX + "px";

      animate(scope.current, { top, left }, { duration: 0 });
    } else {
      setHovered(false);
    }
  };

  useEffect(() => {
    navRef.current?.addEventListener("mousemove", handleMouseMove);

    return () =>
      navRef.current?.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <nav
      ref={navRef}
      onMouseLeave={() => setHovered(false)}
      style={{
        cursor: hovered ? "none" : "auto",
      }}
      className="z-30 glass-nav fixed left-0 right-0 top-0  mx-auto max-w-6xl overflow-hidden border-[1px] border-white/10 bg-gradient-to-br from-white/20 to-white/5 backdrop-blur md:left-6 md:right-6 md:top-6 md:rounded-2xl"
    >
      <div className="glass-nav flex items-center justify-between px-5 py-5">
        <Cursor hovered={hovered} scope={scope} />

        <Links isLoggedIn={isLoggedIn} />

        <Logo />

        <Buttons setMenuOpen={setMenuOpen} isLoggedIn={isLoggedIn} />
      </div>

      <MobileMenu menuOpen={menuOpen} isLoggedIn={isLoggedIn} />
    </nav>
  );
};

const Cursor = ({ hovered, scope }) => {
  return (
    <motion.span
      initial={false}
      animate={{
        opacity: hovered ? 1 : 0,
        transform: `scale(${
          hovered ? 1 : 0
        }) translateX(-50%) translateY(-50%)`,
      }}
      transition={{ duration: 0.15 }}
      ref={scope}
      className="pointer-events-none absolute z-0 grid h-[50px] w-[50px] origin-[0px_0px] place-content-center rounded-full bg-gradient-to-br from-indigo-600 from-40% to-indigo-400 text-2xl"
    >
      <FiArrowUpRight className="text-white" />
    </motion.span>
  );
};

const Logo = () => (
  <span className="pointer-events-none relative left-0 top-[50%] z-10 text-xl md:text-4xl font-black text-white mix-blend-overlay md:absolute md:left-[50%] md:-translate-x-[50%] md:-translate-y-[50%]">
    FizzBuzz
  </span>
);

const Links = ({ isLoggedIn }) => {
  const handleDashboardClick = (e) => {
    if (!isLoggedIn) {
      e.preventDefault();
      window.location.href = '/signin';
    }
  };

  return (
    <div className="hidden items-center gap-2 md:flex">
      <GlassLink text="Home" href={"/"} />
      <GlassLink 
        text="DashBoard" 
        href={"/dashboard/vulnerability"} 
        onClick={handleDashboardClick}
      />
    </div>
  );
};

const GlassLink = ({ text, href, onClick }) => {
  return (
    <a
      href={href}
      onClick={onClick}
      className="group relative scale-100 overflow-hidden rounded-lg px-4 py-2 transition-transform hover:scale-105 active:scale-95"
    >
      <span className="relative z-10 text-white/90 transition-colors group-hover:text-white">
        {text}
      </span>
      <span className="absolute inset-0 z-0 bg-gradient-to-br from-white/20 to-white/5 opacity-0 transition-opacity group-hover:opacity-100" />
    </a>
  );
};

const TextLink = ({ text, href, onClick }) => {
  return (
    <a href={href} onClick={onClick} className="text-white/90 transition-colors hover:text-white">
      {text}
    </a>
  );
};

const Buttons = ({ setMenuOpen, isLoggedIn }) => (
  <div className="flex items-center gap-4">
    {!isLoggedIn && (
      <>
        <div className="hidden md:block">
          <SignInButton />
        </div>
        <a href="/signup">
          <button className="relative scale-100 overflow-hidden rounded-lg bg-gradient-to-br from-indigo-600 from-40% to-indigo-400 px-4 py-2 font-medium text-white transition-transform hover:scale-105 active:scale-95 flex justify-center place-items-center gap-2">
            Sign Up
          </button>
        </a>
      </>
    )}
    {isLoggedIn && (
      <>
        <WelcomeMessage />
        <LogoutButton />
      </>
    )}
    <button
      onClick={() => setMenuOpen((pv) => !pv)}
      className="ml-2 block scale-100 text-3xl text-white/90 transition-all hover:scale-105 hover:text-white active:scale-95 md:hidden"
    >
      <FiMenu />
    </button>
  </div>
);

const SignInButton = () => {
  return (
    <a href="/signin">
      <button className="group relative scale-100 overflow-hidden rounded-lg px-4 py-2 transition-transform hover:scale-105 active:scale-95">
        <span className="relative z-10 text-white/90 transition-colors group-hover:text-white">
          Sign in
        </span>
        <span className="absolute inset-0 z-0 bg-gradient-to-br from-white/20 to-white/5 opacity-0 transition-opacity group-hover:opacity-100" />
      </button>
    </a>
  );
};

const WelcomeMessage = () => (
  <span className="text-white/90">Welcome Back!</span>
);

const LogoutButton = () => {
  const handleLogout = () => {
    localStorage.removeItem('authToken');
  
    window.location.href = '/';
  };

  return (
    <button
      onClick={handleLogout}
      className="group relative scale-100 overflow-hidden rounded-lg px-4 py-2 transition-transform hover:scale-105 active:scale-95 flex items-center gap-2"
    >
      <span className="relative z-10 text-white/90 transition-colors group-hover:text-white">
        Logout
      </span>
      <FiLogOut className="text-white/90 group-hover:text-white" />
      <span className="absolute inset-0 z-0 bg-gradient-to-br from-white/20 to-white/5 opacity-0 transition-opacity group-hover:opacity-100" />
    </button>
  );
};

const MobileMenu = ({ menuOpen, isLoggedIn }) => {
  const [ref, { height }] = useMeasure();

  const handleDashboardClick = (e) => {
    if (!isLoggedIn) {
      e.preventDefault();
      window.location.href = '/signin';
    }
  };

  return (
    <motion.div
      initial={false}
      animate={{
        height: menuOpen ? height : "0px",
      }}
      className="block overflow-hidden md:hidden"
    >
      <div ref={ref} className="flex items-center justify-between px-4 pb-4">
        <div className="flex items-center gap-4">
          <TextLink text="Home" href={"/"} />
          <TextLink text="DashBoard" href={"/dashboard"} onClick={handleDashboardClick} />
        </div>
        {!isLoggedIn && <SignInButton />}
        {isLoggedIn && (
          <>
            <WelcomeMessage />
            <LogoutButton />
          </>
        )}
      </div>
    </motion.div>
  );
};

export default Header;