import React, { Component } from "react";
import { BrowserRouter } from "react-router-dom";
import GlobalHeader from "./components/GlobalHeader";
import "./App.css";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <div className="App">
        <BrowserRouter>
          <GlobalHeader />
        </BrowserRouter>
      </div>
    );
  }
}

export default App;
