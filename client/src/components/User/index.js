import React, { Component } from "react";

class User extends Component {
    constructor(props) {
        super(props);
        this.state = {
            name: props.location.state.name
        };
    }

    render() {
        return <h1> {this.state.name} </h1>;
    }
}

export default User;
