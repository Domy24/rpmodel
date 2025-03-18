import axios from 'axios';
import {errors, loginToasts} from "@/constants/constants.js";
import {useAuthStore} from "@/stores/auth.js";
const API_BASE_URL = 'http://localhost:8000';
const GH_BASE_URL = "https://graphhopper.com/api/1/geocode?"
const ghKey = import.meta.env.VITE_APP_GRAPHHOPPER_API_KEY
console.log(ghKey)

const endpoints = {
  login: `${API_BASE_URL}/auth/jwt/login`,
  register: `${API_BASE_URL}/auth/register`,
  verify: `${API_BASE_URL}/users/me`,
  getVehicles: `${API_BASE_URL}/vehicles`,
  getRoute: `${API_BASE_URL}/route`,
  getUserRoutes: `${API_BASE_URL}/users/me/routes`,

};


const ghEndpoint = {
    autocomplete: (query)  => `${GH_BASE_URL}q=${query}&locale=it&layer=city&key=${ghKey}`
}


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
                  detail: `${error}`,
                  life: 3000,
                };
                reject(error, toast)
            })
    });
}


export const getUserRoutes = () => {
    return new Promise((resolve, reject) => {
        axios
            .get(endpoints.getUserRoutes)
            .then((response) => {
                resolve(response.data)
            })
            .catch((error) => {
                const toast = {
                  severity: 'error',
                  summary: `${errors.internalServerError}`,
                  detail: `${error}`,
                  life: 3000,
                };
                reject({ error, toast })
            })
    })
}

export const getDetailUserRoute = (id) => {
    return new Promise((resolve, reject) => {
        axios
            .get(`${endpoints.getUserRoutes}/${id}`)
            .then((response) => {
                resolve(response.data)
            })
            .catch((error) => {
                console.log(error)
                 const toast = {
                  severity: 'error',
                  summary: `${errors.internalServerError}`,
                  detail: `error`,
                  life: 3000,
                };
                reject({ error, toast })
            })
    })
}

export const completePlaces = (query) => {
    return new Promise((resolve, reject) => {
        console.log(ghEndpoint.autocomplete(query))
        axios
            .get(ghEndpoint.autocomplete(query))
            .then((response) => {
                const list = response.data.hits.map((place) => `${place.name !== undefined ? place.name : ''}${place.country !== undefined ? `, ${place.country}` : ''}${place.state !== undefined ? `, ${place.state}` : ''}`)
                resolve(list)
            })
            .catch((error) => {
                reject(error)
            })
    })
}