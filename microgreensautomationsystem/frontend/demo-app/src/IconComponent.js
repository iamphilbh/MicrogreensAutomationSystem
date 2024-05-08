import React, { useState } from 'react';

function IconComponent() {
  const [isColored, setIsColored] = useState(true);

  const handleClick = () => {
    setIsColored(!isColored);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
      <img 
        src={isColored ? process.env.PUBLIC_URL + '/light_on.png' : process.env.PUBLIC_URL + '/light_off.png'} 
        alt="icon" 
        style={{ width: '100px', cursor: 'pointer' }} 
        onClick={handleClick} 
      />
      <p>Click the icon to change its color</p>
    </div>
  );
}

export default IconComponent;