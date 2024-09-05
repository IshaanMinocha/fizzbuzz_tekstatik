import React from 'react';
import { useLocation } from 'react-router-dom';
import VerticalNavbar from './VerticalNav';
import VulnerabilityTable from './VulnerabilityTable';
import FuzzResultTable from './FuzzResultTable';
import VulnerabilityResolution from './VulnerabilityResolution';

const DashBoard = () => {
  const location = useLocation();
  const path = location.pathname;

  let Content;
  
  if (path === '/dashboard/vulnerability') {
    Content = <VulnerabilityTable />;
  } else if (path === '/dashboard/fuzzresult') {
    Content = <FuzzResultTable />;
  } else if(path  === '/dashboard/resolution'){
    Content = <VulnerabilityResolution/>;
  }
  

  return (
    <div className="flex h-[700px] bg-gray-900 place-items-center">
      <VerticalNavbar />
      <div className="flex-grow p-4 overflow-auto">
        {Content}
      </div>
    </div>
  );
};

export default DashBoard;
