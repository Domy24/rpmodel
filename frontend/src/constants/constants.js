import axios from "axios"
import {useAuthStore} from "@/stores/auth.js";
export const loginToasts = {
    successfulLogin: "Log in completato!",
    failedLogin: "Log in non riuscito!",
    successfulRegister: "Registrazione completata!",
    failedRegister: "Registrazione non completata!",
    homeRedirect: "Sarai reindirizzato alla home.",
    loginRedirect: "Sarai reindirizzato alla pagina di login."
}


export const success = {
    successfulAddedRoute: "Percorso aggiunto correttamente!"
}

export const errors = {
    logoutError: "Errore durante il logout.",
    validationError: "Errore di validazione",
    usernameAlreadyExists: (name, email) => {
        return `Lo username ${name} o l'email: ${email} già esistono.`
    },
    internalServerError: "Errore interno del server",
    detailinternalServerError: "Errore interno.",
    routeNotAdded: "Errore nel salvataggio del percorso"
}

export const pathsName= {
    routeView: "route",
    homeView: "home",
    loginView: "Login",
    registerView: "Register",
    userRoutesView: "Routes",
}
