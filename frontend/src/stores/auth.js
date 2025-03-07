import { defineStore } from 'pinia';

export const useAuthStore = defineStore({
  id: 'authStore',
  state: () => ({
    authToken: null, // Token di autenticazione
  }),
  getters: {
    isAuthenticated: (state) => state.authToken !== null, // Controlla se l'utente è autenticato
  },
  actions: {
    login(token) {
      this.authToken = token; // Imposta il token di autenticazione
    },
    logout() {
      this.authToken = null; // Rimuove il token di autenticazione
    },
    setToken(token) {
      this.authToken = token; // Aggiorna il token di autenticazione
    },
  },
});
