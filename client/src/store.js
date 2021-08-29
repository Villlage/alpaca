import { createStore, applyMiddleware, combineReducers } from "redux";
import reduxThunk from "redux-thunk";
import { createLogger } from "redux-logger";

import userReducer from "./reducers/user";
import adminReducer from "./reducers/admin";

const rootReducer = combineReducers({
    user: userReducer,
    admin: adminReducer
});

const logger = createLogger({ level: "info", collapsed: true });

export default (initialState = {}) => {
    const middlewares = [reduxThunk];

    // Positioning logger at the bottom will only log actions that are going to be applied to the store
    if (process.env.NODE_ENV === "development") {
        middlewares.push(logger);
    }

    const store = createStore(
        rootReducer,
        initialState,
        applyMiddleware(...middlewares)
    );
    return store;
};
