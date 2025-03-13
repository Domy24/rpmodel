<template>
  <div class="map-container">
    <!-- Mappa -->
    <mgl-map
        :map-style="style"
        :center="center"
        :zoom="zoom"
        height="550px"
        class="maplibregl-map"
    >
      <mgl-navigation-control/>
    </mgl-map>
  </div>

  <!-- Spazio tra la mappa e il form -->
  <div class="mt-10">
    <Form
        v-slot=$form
        class="col-span-1 bg-white rounded-lg shadow divide-y divide-gray-200 p-4"
        :initialValues
        :resolver="resolver"
        :validateOnValueUpdate="false"
        :validateOnBlur="true"
        @submit="onFormSubmit"
    >
      <div>
        <div class="w-full sm:w-auto mb-5 content-center">
        <Card>
        <template #content>
            <p class="m-0">
                Inserisci i parametri per il calcolo dell'(eventuale) percorso:
            </p>
        </template>
        </Card>
           </div>
        <div class="flex top-4 justify-between flex-wrap gap-4">

          <div class="w-full sm:w-auto">
              <label for="soc0" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">SoC0</label>
              <InputText id="soc0" name="soc0" type="text" placeholder="Stato di carica iniziale" class="w-full p-2 mb-4"/>
              <Message v-if="$form.soc0?.invalid" severity="error" size="small" variant="simple">
                {{ $form.soc0.error.message }}
              </Message>
            </div>
          <div class="w-full sm:w-auto">
            <label for="socMin" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">SoCmin</label>
            <InputText id="socMin" name="socMin" type="text" placeholder="Stato di carica minimo" class="w-full p-2 mb-4"/>
            <Message v-if="$form.socMin?.invalid" severity="error" size="small" variant="simple">
              {{ $form.socMin.error.message }}
            </Message>
          </div>
          <div class="w-full sm:w-auto">
            <label for="soh" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">SoH</label>
            <InputText id="soh" name="soh" type="text" placeholder="Stato di salute" class="w-full p-2 mb-4"/>
            <Message v-if="$form.soh?.invalid" severity="error" size="small" variant="simple">
              {{ $form.soh.error.message }}
            </Message>
          </div>
                    <div class="w-full sm:w-auto">
            <label for="k" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">Driving style</label>
            <InputText id="k" name="k" type="text" placeholder="Stile di guida" class="w-full p-2 mb-4"/>
            <Message v-if="$form.k?.invalid" severity="error" size="small" variant="simple">
              {{ $form.k.error.message }}
            </Message>
          </div>
        </div>
        <div class="flex top-4 justify-between flex-wrap gap-4">
          <div class="w-full sm:w-auto">
            <label for="nPass" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">N° di passeggeri</label>
            <InputText id="nPass" name="nPass" type="text" placeholder="Numero di passeggeri" class="w-full p-2 mb-4"/>
            <Message v-if="$form.nPass?.invalid" severity="error" size="small" variant="simple">
              {{ $form.nPass.error.message }}
            </Message>
          </div>
          <div class="w-full sm:w-auto">
            <label for="temperature" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">T°</label>
            <InputText id="temperature" name="temperature" type="text" placeholder="Temperatura esterna" class="w-full p-2 mb-4"/>
            <Message v-if="$form.temperature?.invalid" severity="error" size="small" variant="simple">
              {{ $form.temperature.error.message }}
            </Message>
          </div>
          <div class="w-full sm:w-auto">
            <label for="k" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">Driving style</label>
            <InputText id="k" name="k" type="text" placeholder="Stile di guida" class="w-full p-2 mb-4"/>
            <Message v-if="$form.k?.invalid" severity="error" size="small" variant="simple">
              {{ $form.k.error.message }}
            </Message>
          </div>
              <div class="w-full sm:w-auto">
              <label for="k" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">Driving style</label>
              <InputText id="k" name="k" type="text" placeholder="Stile di guida" class="w-full p-2 mb-4"/>
              <Message v-if="$form.k?.invalid" severity="error" size="small" variant="simple">
                {{ $form.k.error.message }}
            </Message>
          </div>
        </div>
       <Button
            :loading="isLoading"
            type="submit"
            label="Calcola percorso"
            icon="pi pi-arrow-circle-right"
            size="small"
            class="border-6 mt-6"
          />
      </div>
    </Form>
  </div>
</template>

<script>
import {MglMap, MglNavigationControl} from '@indoorequal/vue-maplibre-gl';
import {InputText, Button} from 'primevue';
import {ref} from 'vue';
import {Form} from "@primevue/forms";
import {yupResolver} from "@primevue/forms/resolvers/yup";
import {parametersValidationSchema} from "@/validators/validators.js";

export default {
  name: "MapComponent",
  components: {
    MglMap,
    MglNavigationControl,
    InputText,
    Button,
    Form
  },
  data() {
    return {
      style: 'https://api.maptiler.com/maps/streets-v2/style.json?key=ssYZIhglJGSf9GYsHiOO',
      center: [12.550343, 55.665957],
      zoom: 8,
      soc0: "",
      socMin: "",
      soh: "",
      nPass: "",
      temperature: "",
      k: "",
      isLoading: false,
      resolver: yupResolver( parametersValidationSchema() )
    }
  },
  methods: {
    onFormSubmit({ valid, values }) {
      if(valid){
        alert("corretto")
      }
    }
  }
}
</script>

<style lang="scss">
@import "maplibre-gl/dist/maplibre-gl.css";

.map-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.maplibregl-map {
  width: 100%;
  height: 550px;
}

.form-container {
  width: 100%;
  max-width: 600px;
  margin-top: 20px;
  padding: 20px;
  border-radius: 8px;
}

.field {
  margin-bottom: 1rem;
}

button {
  width: 100%;
}
</style>
