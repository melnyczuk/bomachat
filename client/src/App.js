import React, { Component } from 'react';
import axios from 'axios';
import './App.scss';

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      reply: "",
      input: "",
      logs: [],
      axios: axios.create({
        baseURL: "https://bomachat.herokuapp.com/8070",
        timeout: 10000,
        headers: {
          "Access-Control-Allow-Origin": "*"
        }
      }),
    }
    this.handleChange = this.handleChange.bind(this)
    this.handleKeyPress = this.handleKeyPress.bind(this)
    this.handleKeyDown = this.handleKeyDown.bind(this)
    this.buildParagraph = this.buildParagraph.bind(this)
    this.interactChatbot = this.interactChatbot.bind(this)
  }

  // Methods to control the chat log that appears on screen.
  // Chat log is stored as a list of <p> tag elements with dated keys.
  handleChange(logValue, origin) {
    const logs = this.state.logs
    if (logs.length > 10) logs.shift()
    logs.push(this.buildParagraph(logValue, origin))
    this.setState({ logs: logs })
  }

  buildParagraph(logValue, origin) {      
    return (<p className={origin} key={Date.now()}>{logValue}</p>)
  }

  // Methods to control input from User.
  handleKeyPress(event) {
    if (event.key !== 'Enter') {
      this.setState({ input: this.state.input + event.key })
    } else if (event.key === 'Enter' && this.state.input !== "") {
      this.setState({ input: "" })
      this.handleEnter(event)
    }
  }

  handleKeyDown(event) {
    if (event.key === 'Backspace') this.setState({ input: this.state.input.slice(0, this.state.input.length - 1) })
  }

  // These need to pass "chatbotInput" to chatbot.
  handleEnter(event) {
    const chatbotInput = event.target.value
    this.handleChange(chatbotInput, "usr")
    this.interactChatbot(chatbotInput)
  }

  // Methods to pass request and response between react app and chatbot
  interactChatbot(request) {
    this.state.axios.post('/chat', {body:request})
    .then((response) => {
      if(response.status === 200) {
        this.handleChange(response.data, "bot")
      }
    }).catch(function(error){console.log(error)})
  }

  // RENDER RESULTS
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src='../static/boma.png' className="App-logo" alt="logo" />
        </header>
        <div>
          <div id="App-readout">
            {this.state.logs}
          </div>
          <input 
            id="userInput" 
            type="text" 
            value={this.state.input} 
            onKeyDown={this.handleKeyDown} 
            onKeyPress={this.handleKeyPress} 
            tabindex="-1"
          />
        </div>
        <div onLoad={this.loadFiles}/>
      </div>
    );
  }
}

export default App;
