import axios from 'axios';
import {errors, loginToasts} from "@/constants/constants.js";
import {useAuthStore} from "@/stores/auth.js";
const API_BASE_URL = 'http://localhost:8000';



const endpoints = {
  login: `${API_BASE_URL}/auth/jwt/login`,
  register: `${API_BASE_URL}/auth/register`,
};



export const login = (username, password) => {
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




