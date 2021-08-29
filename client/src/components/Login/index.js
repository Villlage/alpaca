import React from "react";
import useForm from "react-hook-form";
import { useSelector, useDispatch } from "react-redux";
import { Login } from "./../../actions/user";
import "./styles.css";

export default function LoginForm(props) {
    const { register, handleSubmit, errors } = useForm();
    const dispatch = useDispatch();
    const apiError = useSelector(state => state.user.error);

    const onSubmit = data => {
        dispatch(Login(data));
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <input
                type="text"
                name="email"
                placeholder="Email"
                ref={register({ required: true })}
            />
            {errors.email && <p> "Email is required" </p>}
            {apiError && <p> {apiError} </p>}

            <input
                type="password"
                name="password"
                placeholder="Password"
                ref={register({ required: true })}
            />
            {errors.password && <p> "Password is required" </p>}

            <input type="submit" />
        </form>
    );
}
