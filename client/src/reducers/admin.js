import { ADMIN } from "../actions/types";

export default function adminReducer(state = {}, action) {
    const { type } = action;
    switch (type) {
        case ADMIN:
            return {
                ...state
            };
        default:
            return state;
    }
}
