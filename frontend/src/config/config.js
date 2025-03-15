import axios from "axios";

export default function configureAxios(authStore) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${authStore.authToken}`;
  axios.defaults.headers.common['Content-Type'] = 'application/json';
}

