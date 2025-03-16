import {defineStore} from 'pinia';
import router from "@/router/index.js";
import {verify} from "@/backend/backend.js";

export const useAuthStore = defineStore("authStore", {
    id: 'authStore',
    state: () => ({
        authToken: null,
    }),
    getters: {

    },
    actions: {
        login(token) {
            this.setToken(token);
        },
        logout() {
            this.authToken = null;
            localStorage.removeItem('token');
        },
        setExpiration(expiration){
            this.isExpired = expiration
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
        },
        verifyToken() {
            console.log(this.authToken)
            if(this.authToken){
                return verify(this.authToken)
            }else{
                return false;
            }
        },
    },

});
