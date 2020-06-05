import React, { useState, useEffect } from 'react';
import axios from 'axios';

import ChatLog from './ChatLog';
import InputBar from './InputBar';

const { post } = axios.create({
  baseURL: "https://bomachat.herokuapp.com",
  timeout: 100000,
  headers: {
    "Access-Control-Allow-Origin": "*"
  }
});

function reduceLogs(logs, log) {
  if (logs.length < 10) {
    return [...logs, log];
  } else {
    const [, ...fresh] = logs;
    return([...fresh, log]);
  }
}

const Gail = () => {
  const [chatLogs, setLogs] = useState([]);
  const [latest, setLatest] = useState('');

  const callBot = async () => {
    if (latest === '') return;

    try {
      const response = await post('/chat', { body: latest });
      const botMsg = `bot:${response.data}`;
      const logs = reduceLogs(chatLogs, botMsg);
      setLogs(logs);
    }
    
    catch (e) {
      const logs = reduceLogs(chatLogs, 'bot:And how does that make you feel?');
      setLogs(logs);
    }
  }

  useEffect(() => { callBot(); }, [latest]);

  return (
    <div>
      <ChatLog logs={chatLogs} />
      <InputBar 
        onSubmit={(useInput) => { 
          const logs = reduceLogs(chatLogs, `usr:${useInput}`);
          setLogs(logs); 
          setLatest(useInput); 
        }}
      />
    </div>
  );
}

export default Gail;
