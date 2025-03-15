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
        getToken(){
            const token = localStorage.getItem('token');
            if (token){
                this.setToken(token)
            }else{

            }
        },
        setToken(token) {
            this.authToken = token;
            localStorage.setItem('token', token);
        },
        initializeAuthStore() {
            const token = localStorage.getItem('token')
            console.log(token)
            if (token) {
                this.login(token);
                router.push({name: "home"})
            }
        },
        verifyToken() {
            if(this.authToken){
                verify(this.authToken)
                .then((response) => true)
                .catch((error) => false)
            }else{
                return false;
            }
        },
    },

});
