import * as yup from "yup";

export const registerValidationSchema = () => {
    return yup.object().shape({
        username: yup.string().required('Username is required'),
        email: yup.string().email('Invalid email format').required('Email is required'),
        password: yup.string().min(6, 'Password must be at least 6 characters').required('Password is required'),
    });
}

export const logInValidationSchema = () => {
    return yup.object().shape({
        username: yup.string().email('Invalid email format').required('Email is required'),
        password: yup.string().min(6, 'Password must be at least 6 characters').required('Password is required'),
    });
}
          // soc0: "",
          // socMin: "",
          // soh: "",
          // nPass: "",
          // temperature: "",
          // start: "",
          // end: "",
          // vehicles: null,
          // drivingStyle: null
export const parametersValidationSchema = ()  => {
    return yup.object().shape({
            socMin: yup.number()
                .min(0, "SoCmin deve essere positivo")
                .lessThan(100, "SoCmin deve essere minore del 100%")
                .required("socMin è obbligatorio"),
            soc0: yup
              .number()
              .when('socMin', (socMin, schema) =>
                schema.min(socMin, `Soc0 deve essere almeno pari a SoCmin (${socMin})`)
              ).max(100, "SoC0 non può superare il 100%")
              .required("SoC0 è obbligatorio"),
            soh: yup.number()
                .min(60, "Non è possibile inserire valori minori del 60%.")
                .max(100,"Non è possibile inserire valori superiori al 100%." )
                .required(),
            nPass: yup.number()
                .integer("Il numero di passeggeri deve essere un intero.")
                .min(0, "Non meno di 0 passeeggeri.")
                .max(4, "Numero di passeggeri limitato a 5"),
            temperature: yup.number()
                .min(-50, "Inserire valori superiori a -50°")
                .max(50,"Inserire valori inferiori a 50°" )
                .required(),
            start: yup.string().required("E' necessario un punto di partenza."),
            end: yup.string().required("E' necessario un punto di destinazione."),
            vehicles: yup.object().required(),
            drivingStyle: yup.object().required()
                // yup.number()
                // .oneOf([0.5, 0.6, 0.9], "Stile di guida errato!")
                // .required(),
    });
}