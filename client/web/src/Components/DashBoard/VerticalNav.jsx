import React from "react";
import { useLocation } from "react-router-dom";
import { GrVulnerability } from "react-icons/gr";
import { HiChartBar } from "react-icons/hi2";
import { VscCommentUnresolved } from "react-icons/vsc";
import { FaBook } from "react-icons/fa6";
import { IoAnalytics } from "react-icons/io5";

const VerticalNavbar = () => {
  const location = useLocation();
  const path = location.pathname;

  const isActive = (route) =>
    path === route
      ? "bg-indigo-600 text-white"
      : "text-gray-400 hover:text-white";
  const handleLogout = () => {
    localStorage.removeItem("authToken");

    window.location.href = "/";
  };
  return (
    <div className="hidden md:flex md:w-64 md:flex-col">
      <div className="flex flex-col flex-grow h-[400px] bg-gray-800 justify-center ml-6 rounded-lg">
        <div className="flex flex-col flex-1 px-3 justify-center">
          <div className="space-y-4">
            <nav className="flex-1 space-y-6">
              <a
                href="/dashboard/"
                className={`flex items-center px-4 py-2.5 text-sm font-medium transition-all duration-200 rounded-lg group ${isActive(
                  "/dashboard/"
                )}`}
              >
                <IoAnalytics className="mr-3" />
                Home
              </a>
              <a
                href="/dashboard/vulnerability"
                title=""
                className={`flex items-center px-4 py-2.5 text-sm font-medium transition-all duration-200 rounded-lg group ${isActive(
                  "/dashboard/vulnerability"
                )}`}
              >
                <GrVulnerability className="mr-3" />
                Vulnerability
              </a>

              <a
                href="/dashboard/fuzzresult"
                className={`flex items-center px-4 py-2.5 text-sm font-medium transition-all duration-200 rounded-lg group ${isActive(
                  "/dashboard/fuzzresult"
                )}`}
              >
                <HiChartBar className="mr-3" />
                Fuzz Requests
              </a>

              <a
                href="/dashboard/resolution"
                className={`flex items-center px-4 py-2.5 text-sm font-medium transition-all duration-200 rounded-lg group ${isActive(
                  "/dashboard/resolution"
                )}`}
              >
                <VscCommentUnresolved className="mr-3" />
                Resolution
              </a>

              <a
                target="_blank"
                href="https://www.freecodecamp.org/news/web-security-fuzz-web-applications-using-ffuf/"
                className={`flex items-center px-4 py-2.5 text-sm font-medium transition-all duration-200 rounded-lg group ${isActive(
                  "#"
                )}`}
              >
                <FaBook className="mr-3" />
                Learn
              </a>
            </nav>

            <hr className="border-gray-700" />

            <nav className="flex-1 space-y-2">
              <button
                onClick={handleLogout}
                className="flex items-center px-4 py-2.5 text-sm font-medium transition-all duration-200 text-black w-full justify-center hover:text-white rounded-lg hover:bg-indigo-600 group bg-white"
              >
                Logout
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VerticalNavbar;
