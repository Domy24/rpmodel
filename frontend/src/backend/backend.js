import axios from 'axios';
import {errors, loginToasts} from "@/constants/constants.js";
import {useAuthStore} from "@/stores/auth.js";
const API_BASE_URL = 'http://localhost:8000';



const endpoints = {
      login: `${API_BASE_URL}/auth/jwt/login`,
      register: `${API_BASE_URL}/auth/register`,
      verify: `${API_BASE_URL}/users/me`,
      getVehicles: `${API_BASE_URL}/vehicles`,
      getRoute: `${API_BASE_URL}/route`,
};



export const login = (username, password) => {
    console.log("di nuovo")
  return new Promise((resolve, reject) => {
    axios
      .post(
        endpoints.login,
        new URLSearchParams({ username, password }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      )
      .then((response) => {
        const data = response.data;
        console.log(data.access_token)
        useAuthStore().setToken(data.access_token);
        const toast = {
          severity: 'success',
          summary: `${loginToasts.successfulLogin}`,
          detail: `${loginToasts.homeRedirect}`,
          life: 3000,
        };
        resolve({ data, toast, redirect: "/" });
      })
      .catch((error) => {
        const toast = {
          severity: 'error',
          summary: `${loginToasts.failedLogin}`,
          detail: `${loginToasts.loginRedirect}`,
          life: 3000,
        };
        reject({toast, error} );
      });
  });
};

export const register = (userData) => {
  return new Promise((resolve, reject) => {
    axios
      .post(endpoints.register, userData, {
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then((response) => {
        const toast = {
          severity: 'success',
          summary: `${loginToasts.successfulRegister}`,
          detail: `${loginToasts.loginRedirect}`,
          life: 3000,
        };
        resolve({ data: response.data, toast, redirect: "/auth/login"});
      })
      .catch((error) => {
        const toast = {
          severity: 'error',
          summary: `${loginToasts.failedRegister}`,
          detail: `${errors.usernameAlreadyExists(userData.username)} Oppure c'è un errore interno.`,
          life: 3000,
        };
        reject({ toast, error });
      });
  });
};

export const verify = (token) => {
  return new Promise((resolve, reject) => {
      axios
          .get(endpoints.verify)
          .then((response) =>{
            if(response) resolve(response.data)
          })
          .catch((error) => {
            reject(error)
          })
  });
}

export const getVehicles = () => {
  return new Promise((resolve, reject) => {
      axios
          .get(endpoints.getVehicles)
          .then(
              (response) => {
                if(response) resolve(response.data)
              }
          )
          .catch((error) => {
            reject(error)
          })
  });
}

// parameters = {
//   "start": "string",
//   "end": "string",
//   "route_parameters": {
//     "soc0": 0,
//     "soc_min": 0,
//     "soh": 0,
//     "k": 0,
//     "t": 0,
//     "n_pass": 0
//   },
//   "vehicle_parameters": {
//     "model": "string",
//     "weight_kg": 0,
//     "cd_area": 0,
//     "velocity_mps": 0,
//     "motor_efficiency": 0,
//     "front_area": 0,
//     "mu_r": 0,
//     "vtype": "string",
//     "energy_usable": 0
//   }
// }


export const getRoute = (parameters) => {
    return new Promise((resolve, reject) =>{
        axios
            .post(endpoints.getRoute, {
                 parameters
            })
            .then((response) => {
                resolve(response.data)
            })
            .catch((error) => {
                const toast = {
                  severity: 'error',
                  summary: `${errors.internalServerError}`,
                  detail: `${errors.detailinternalServerError}`,
                  life: 3000,
                };
                reject(error, toast)
            })
    });
}

