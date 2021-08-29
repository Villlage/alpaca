import React from "react";
import { Route, Switch } from "react-router";

import RegisterForm from "./components/Register";
import LoginForm from "./components/Login";
import User from "./components/User";

function App() {
    return (
        <Switch>
            <Route exact path={"/register"} component={RegisterForm} />
            <Route exact path={"/login"} component={LoginForm} />
            <Route exact path={"/user"} component={User} />
        </Switch>
    );
}

export default App;
