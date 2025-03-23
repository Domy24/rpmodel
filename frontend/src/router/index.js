import {createRouter, createWebHistory} from 'vue-router'
import {pathsName} from "@/constants/constants.js";
import HomeView from '../views/HomeView.vue'
import LoginView from "@/views/auth/LoginView.vue";
import RegisterView from "@/views/auth/RegisterView.vue";
import MapComponent from "@/components/MapComponent.vue";
import {useAuthStore} from "@/stores/auth.js";
import UserRoutesComponent from "@/components/UserRoutesComponent.vue";
import {verify} from "@/backend/backend.js";




const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: pathsName.homeView,
            component: HomeView,
        },
        {
            path: "/auth",
            redirect: "login",
            children: [
                {
                    path: "login",
                    name: pathsName.loginView,
                    component: LoginView
                },
                {
                    path: "register",
                    name: pathsName.registerView,
                    component: RegisterView
                },

            ]
        },
        {
            path: "/route",
            name: pathsName.routeView,
            component: MapComponent,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: "/users",
            redirect: "me",
            children: [
                {
                    path: "routes",
                    name: pathsName.userRoutesView,
                    component: UserRoutesComponent,
                    meta: {
                        requiresAuth: true
                    }
                }
            ]
        },

    ],
})


router.beforeEach((to, from, next) => {
const authStore = useAuthStore();
    if(authStore.authToken){
        verify(authStore.authToken)
            .then((response) => {
                if ([pathsName.loginView, pathsName.registerView].includes(to.name)) {
                    next({ name: pathsName.homeView });
                }
            })
            .catch((error) => {
                next({ name: pathsName.loginView })
            });
    }else{
        if ([pathsName.routeView].includes(to.name)) {
                next({ name: pathsName.loginView });
        }
    }


    if (to.matched.some(record => record.meta.requiresAuth)) {
        verify(authStore.authToken)
            .then((response) => {
                next()
            })
            .catch((error) => {
                next({ name: pathsName.loginView, query: { redirect: to.fullPath } });
            })
    } else {
        next();
    }
});


export default router
