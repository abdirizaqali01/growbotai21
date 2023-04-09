import React, { Component } from "react";
import { render } from "react-dom";
import LandingPage from "./LandingPage";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (<LandingPage/>);
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);