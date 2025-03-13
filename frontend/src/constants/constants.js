export const loginToasts = {
    successfulLogin: "Log in completato!",
    failedLogin: "Log in non riuscito!",
    successfulRegister: "Registrazione completata!",
    failedRegister: "Registrazione non completata!",
    homeRedirect: "Sarai reindirizzto alla home.",
    loginRedirect: "Sarai reindirizzto alla pagina di login."
}

export const errors = {
    validationError: "Errore di validazione",
    usernameAlreadyExists: (name) => {
        return `Lo username ${name} già esiste.`
    }
}

export const pathsName= {
    routeView: "route",
    homeView: "home",
    loginView: "Login",
    registerView: "Register"
}