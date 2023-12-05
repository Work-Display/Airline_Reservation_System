import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://127.0.0.1:8000"
});


//  In the context of Redux, a thunk allows you to dispatch a function instead of a plain action object, 
// enabling you to perform asynchronous operations and control the flow of actions based on their results.
export const fetchUser = createAsyncThunk(
  'user/fetchUser',
  async () => {
    try {
      const response = await client.get('/user/models/my-own-user/');
      return response.data;
    } catch (error) {
      console.log("This is why user is null: ", error.response.data);
      throw error.response.data;
    }
  }
);

const userSlice = createSlice({
  name: 'user',
  initialState: { user: null, status: 'idle', error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(fetchUser.pending, (state) => {
      state.status = 'loading';
    });
    builder.addCase(fetchUser.fulfilled, (state, action) => {
      state.status = 'succeeded';
      state.user = action.payload;
    });
    builder.addCase(fetchUser.rejected, (state, action) => {
      state.status = 'failed';
      state.error = action.error.message;
      state.user = null;
    });
  },
});

export const updateUser = createAsyncThunk('user/updateUser', async (args, { dispatch }) => {
  await dispatch(fetchUser());
});

export default userSlice.reducer;