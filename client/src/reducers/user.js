import { REGISTER, LOGIN } from "../actions/types";

export default function userReducer(state = {}, action) {
    const { type } = action;
    switch (type) {
        case REGISTER:
            return {
                ...state,
                error: action.error
            };
        case LOGIN:
            return {
                ...state,
                error: action.error
            };

        default:
            return state;
    }
}
