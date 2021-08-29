import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import RegisterForm from "./components/Register";
import renderer from "react-test-renderer";
import { shallow, mount, render } from "enzyme";

it("renders without crashing", () => {
    shallow(<App />);
});
