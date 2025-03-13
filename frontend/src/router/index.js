import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from "@/views/auth/LoginView.vue";
import RegisterView from "@/views/auth/RegisterView.vue";
import MapComponent from "@/components/MapComponent.vue";
import {useAuthStore} from "@/stores/auth.js";
import {pathsName} from "@/constants/constants.js";

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
                    component: RegisterView
                },

            ]
        },
        {
            path: "/route",
            name: "route",
            component: MapComponent,
            meta: {
                requiresAuth: true
            }
        }
    ],
})

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();

    if ([pathsName.loginView, pathsName.registerView].includes(to.name) && authStore.authToken) {
        next({ name: 'home' });
        return;
    }

    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!authStore.authToken) {
            next({ name: pathsName.loginView, query: { redirect: to.fullPath } });
        } else {
            next();
        }
    } else {
        next();
    }
});


export default router
