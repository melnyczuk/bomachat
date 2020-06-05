import React, { useState } from 'react';

const InputBar = ({ onSubmit }) => {
  const [userInput, setUserInput] = useState(''); 

  function handleDelete() {
    setUserInput(userInput.slice(0, userInput.length - 1));
  }

  function handleKeyPress(event) {
    if (event.key === 'Backspace') {
      handleDelete();
      return;
    }

    if (event.key === 'Enter' && userInput !== '') {
      onSubmit(userInput);
      setUserInput('');
      return;
    }

    setUserInput(`${userInput}${event.key}`);
    return;
  }

  function handleKeyDown(event) {
    if (event.key === 'Backspace') {
      handleDelete();
      return;
    }
  }

  return (<input 
    readOnly
    id="userInput" 
    type="text" 
    value={userInput}
    onKeyDown={handleKeyDown} 
    onKeyPress={handleKeyPress}
    tabIndex={-1}
    />);
  }

export default InputBar;
