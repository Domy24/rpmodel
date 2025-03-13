import {defineStore} from 'pinia';
import router from "@/router/index.js";

export const useAuthStore = defineStore("authStore", {
    id: 'authStore',
    state: () => ({
        authToken: null,
    }),
    getters: {
        isAuthenticated: (state) => state.authToken !== null,
    },
    actions: {
        login(token) {
            this.setToken(token);
        },
        logout() {
            this.authToken = null;
            localStorage.removeItem('token');
        },
        setToken(token) {
            this.authToken = token;
            localStorage.setItem('token', token);
        },
        initializeAuthStore() {
            const token = localStorage.getItem('token')
            if (token) {
                this.login(token);
                router.push({name: "home"})
            }
        }
    },

});
