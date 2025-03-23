import './assets/main.css'
import ToastService from 'primevue/toastservice';
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config';
import App from './App.vue'
import router from './router'
import {definePreset} from '@primeuix/themes';
import Aura from '@primeuix/themes/aura';
import Button from "primevue/button";
import Menubar from 'primevue/menubar';
import {Form} from "@primevue/forms";
import {InputText, Message, Toast} from "primevue";
const app = createApp(App)
const pinia = createPinia()
import VueMaplibreGl from '@indoorequal/vue-maplibre-gl'
import Card from "primevue/card";
import {useAuthStore} from "@/stores/auth.js";
import axios from "axios";
import configureAxios from "@/config/config.js";

app.use(pinia)
app.use(ToastService)
app.use(router)
app.use(VueMaplibreGl)

app.config.globalProperties.$authStore = useAuthStore();

const MyPreset = definePreset(Aura, {
    semantic: {
        primary: {
            50: '#F8F0EB',
            100: '#F2E4D8',
            200: '#A8794B',
            300: '#D1AE91',
            400: '#E2C9B5',
            500: '#C1946D',
            600: '#8B5E3D',
            700: '#704831',
            800: '#573226',
            900: '#3D1E17',
            950: '#27120D',
        }
    }
});
app.use(PrimeVue,{
    theme:{
        prefix: "p",
        preset: MyPreset
    }
})

app.component("Button", Button)
app.component("Menubar", Menubar)
app.component("Form", Form)
app.component("InputText", InputText)
app.component("Message", Message)
app.component("Toast", Toast)
app.component("Card", Card)

const authStore = useAuthStore()
authStore.initializeAuthStore();
configureAxios(authStore)

app.mount('#app')






