import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from "@/views/auth/LoginView.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
        },
        {
            path: '/about',
            name: 'about',
            component: () => import('../views/AboutView.vue'),
        },
        {
            path: "/auth",
            redirect: "login",
            children: [
                {
                    path: "login",
                    name: "Login",
                    component: LoginView
                },
                {
                    path: "register",
                    name: "Register",
                    component: LoginView
                },

            ]
        }
    ],
})

export default router
