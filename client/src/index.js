import React from "react";
import ReactDOM from "react-dom";
import { Router } from "react-router-dom";
import createStore from "./store";

import history from "./history";
import { Provider } from "react-redux";
import App from "./App";

import "./index.css";
import * as serviceWorker from "./serviceWorker";

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA

export const store = createStore(window.__preloaded_state__ || {});

ReactDOM.render(
    <Provider store={store}>
        <Router history={history}>
            <App />
        </Router>
    </Provider>,
    document.getElementById("root")
);

serviceWorker.unregister();
