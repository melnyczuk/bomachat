import React from 'react';

const ChatLog = ({ logs = [] }) => (
  <div id="App-readout">
    {
      logs.length !== 0 && logs
        .map(log => log.split(':'))
        .map(([originator, message]) => <p key={message} className={originator}>{message}</p>)
    }
  </div>
);

export default ChatLog;
