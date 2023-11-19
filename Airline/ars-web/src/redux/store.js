import { configureStore } from '@reduxjs/toolkit';
import userReducer, { updateUser } from './user';

const store = configureStore({
  reducer: {
    user: userReducer
  },
});

store.subscribe(() => {
  const state = store.getState();
  // Save the user state to local storage if needed
  // localStorage.setItem('user', JSON.stringify(state.user.user));
});

store.dispatch(updateUser()); // Dispatch this action on application startup

export default store;