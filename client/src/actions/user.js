import { REGISTER, LOGIN } from "./types";
import history from "./../history";

import axios from "axios";

export const Register = data => {
    return dispatch => {
        return axios
            .post(`register`, { email: data.email, password: data.password })
            .then(response => {
                dispatch({
                    type: REGISTER,
                    error: null
                });
            })
            .catch(error => {
                dispatch({
                    type: REGISTER,
                    error: error
                });
            });
    };
};

export const Login = data => {
    return dispatch => {
        return axios
            .post(`login`, { email: data.email, password: data.password })
            .then(response => {
                history.push({ pathname: "/user", state: { name: "gilad" } });
            })
            .catch(error => {
                dispatch({
                    type: LOGIN,
                    error: error.response.data
                });
            });
    };
};
