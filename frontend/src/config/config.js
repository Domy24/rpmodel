import axios from "axios";

export default function configureAxios(authStore) {
  axios.defaults.headers.common['Content-Type'] = 'application/json';

    axios.interceptors.request.use((config) => {
    if (config.url && config.url.includes('graphhopper.com')) {
      delete config.headers['Authorization'];
    } else {
      config.headers['Authorization'] = `Bearer ${authStore.authToken}`;
    }
    return config;
  });
}

