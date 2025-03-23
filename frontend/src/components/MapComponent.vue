<template>
  <div class="map-container">
    <mgl-map
        :key="mapKey"
        :map-style="style"
        :center="center"
        :zoom="zoom"
        height="550px"
        class="maplibregl-map"
        >
          <mgl-geo-json-source
          source-id="geojson"
          :data="geojsonSource"
        >
          <mgl-line-layer
            layer-id="geojson"
            :layout="layout"
            :paint="paint"
          />
      </mgl-geo-json-source>
      <mgl-navigation-control/>
           <mgl-marker
              v-for="(marker, index) in markers"
              :key="index"
              :coordinates="[marker.lat, marker.lon]"
              color="#cc0000"
            />
    </mgl-map>
  </div>

  <!-- Spazio tra la mappa e il form -->
  <div class="mt-10">
    <Form
        v-slot=$form
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

          <div class="w-full ">
              <label for="soc0" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">SoC0</label>
              <InputText id="soc0" name="soc0" type="text" placeholder="Stato di carica iniziale" class="w-full p-2 mb-4"/>
              <Message v-if="$form.soc0?.invalid" severity="error" size="small" variant="simple">
                {{ $form.soc0.error.message }}
              </Message>
            </div>
          <div class="w-full ">
            <label for="socMin" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">SoCmin</label>
            <InputText id="socMin" name="socMin" type="text" placeholder="Stato di carica minimo" class="w-full p-2 mb-4"/>
            <Message v-if="$form.socMin?.invalid" severity="error" size="small" variant="simple">
              {{ $form.socMin.error.message }}
            </Message>
          </div>
          <div class="w-full ">
            <label for="soh" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">SoH</label>
            <InputText id="soh" name="soh" type="text" placeholder="Stato di salute" class="w-full p-2 mb-4"/>
            <Message v-if="$form.soh?.invalid" severity="error" size="small" variant="simple">
              {{ $form.soh.error.message }}
            </Message>
          </div>
          <div class="w-full ">
            <label for="drivingStyle" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">Driving style</label>
                  <TreeSelect name="drivingStyle" :options="drivingStyleOptions" placeholder="Select a driving style" class="w-full sm:w-64" />
          </div>
          <div class="w-full">
            <label for="start" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">Partenza</label>
            <AutoComplete id="start" name="start" type="text" placeholder="Partenza" :suggestions="suggestions" @complete="complete" :style="{ border: 'none', boxShadow: 'none', padding: 0}"/>
            <Message v-if="$form.start?.invalid" severity="error" size="small" variant="simple">
              {{ $form.start.error.message }}
            </Message>
          </div>
        </div>
        <div class="flex top-4 justify-between flex-wrap gap-4">
          <div class="w-full ">
            <label for="nPass" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">N° di passeggeri</label>
            <InputText id="nPass" name="nPass" type="text" placeholder="Numero di passeggeri" class="w-full p-2 mb-4"/>
            <Message v-if="$form.nPass?.invalid" severity="error" size="small" variant="simple">
              {{ $form.nPass.error.message }}
            </Message>
          </div>

          <div class="w-full ">
            <label for="temperature" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">T°</label>
            <InputText id="temperature" name="temperature" type="text" placeholder="Temperatura esterna" class="w-full p-2 mb-4"/>
            <Message v-if="$form.temperature?.invalid" severity="error" size="small" variant="simple">
              {{ $form.temperature.error.message }}
            </Message>
          </div>
          <div class="w-full ">
            <label for="vehicles" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">Select one vehicle</label>
                  <TreeSelect name="vehicles" :options="vehiclesOptions" placeholder="Select a vehicle" class="w-full sm:w-64" />
          </div>
          <div class="w-full ">
            <label for="end" class="text-surface-900 dark:text-surface-0 font-medium mb-2 block">Destinazione</label>
            <AutoComplete id="end" name="end" type="text" placeholder="Destinazione" :suggestions="suggestions" @complete="complete" :style="{ border: 'none', boxShadow: 'none' , padding: 0}"/>
            <Message v-if="$form.end?.invalid" severity="error" size="small" variant="simple">
              {{ $form.end.error.message }}
            </Message>
            <Message v-if="score" severity="info" size="large" variant="simple">
              {{ `Score: ${this.score}` }}
            </Message>
          </div>
        </div>
        <Button
              v-if="canAddRoute"
              :loading="addRouteIsLoading"
              type="button"
              label="Salva percorso"
              icon="pi pi-plus-circle"
              size="small"
              @click="addRoute"
              style="margin-bottom: 20px;"
              class="border-6 mt-6"
          />
       <Button
            :loading="isLoading"
            type="submit"
            label="Calcola percorso"
            icon="pi pi-arrow-circle-right"
            size="small"
            style="margin-bottom: 20px;"
            class="border-6 mt-6"
          />
          <Message v-if="routeNotFound" severity="error" size="small" style="padding: 12px" variant="simple">
          No route found.
        </Message>
      </div>
    </Form>
  </div>
</template>

<script>
import {MglMap, MglNavigationControl, MglGeoJsonSource, MglLineLayer} from '@indoorequal/vue-maplibre-gl';
import {InputText, Button, useToast, AutoComplete} from 'primevue';
import {Form} from "@primevue/forms";
import {yupResolver} from "@primevue/forms/resolvers/yup";
import {parametersValidationSchema} from "@/validators/validators.js";
import TreeSelect from 'primevue/treeselect';
import {addRoute, completePlaces, getRoute, getVehicles} from "@/backend/backend.js";
import {toRaw} from "vue";
import {errors, success} from "@/constants/constants.js";
const key = import.meta.env.VITE_MAPTILER_KEY

export default {
  name: "MapComponent",
  components: {
    MglMap,
    MglNavigationControl,
    MglGeoJsonSource,
    MglLineLayer,
    InputText,
    Button,
    Form,
    TreeSelect,
    AutoComplete
  },
  data() {
    return {
      initialValues: {
          soc0: null,
          socMin: null,
          soh: null,
          nPass: null,
          temperature: null,
          start: "",
          end: "",
          vehicles: null,
          drivingStyle: null
        },
          score: null,
          canAddRoute: false,
          suggestions: null,
          style: `https://api.maptiler.com/maps/streets-v2/style.json?key=${key}`,
          center:  [ 12.481633, 41.894431 ],
          zoom: 5,
          vehiclesOptions : null,
          vehiclesParam : null,
          drivingStyleOptions : null,
          markers: [],
          resolver: yupResolver( parametersValidationSchema() ),
          isLoading: false,
          addRouteIsLoading: false,
          geojsonSource: {
          type: 'FeatureCollection',
          features: [
            {
              type: 'Feature',
              properties: {},
              geometry: {
                type: 'LineString',
                coordinates: [],
              },
            },
        ],
      },
      layout: {
        'line-join': 'round',
        'line-cap': 'round',
      },
      paint: {
        'line-color': '#FF0000',
        'line-width': 8,
      },
      mapKey: 0,
      routeNotFound: false
    }
  },
  methods: {
    onFormSubmit({ valid, values }) {
      const drivingStyleValue = toRaw(values.drivingStyle);
      const vehiclesValue = toRaw(values.vehicles);
      const dkey = Object.keys(drivingStyleValue)[0];
      const skey = Object.keys(vehiclesValue)[0];
      this.isLoading = true
      this.canAddRoute = false
      if(valid){
        const selectedStyle = this.drivingStyleOptions.find(option => option.key == dkey);
        const selectedVehicle = this.vehiclesOptions.find(option => option.key == skey);
        this.start = values.start
        this.end = values.end
        const body =JSON.parse(JSON.stringify({
          start: values.start,
          end: values.end,
          route_parameters: {
            soc0: values.soc0,
            soc_min: values.socMin,
            soh: values.soh,
            k: selectedStyle.data,
            t: values.temperature,
            n_pass: values.nPass,
          },
          vehicle_parameters: toRaw(selectedVehicle.data)
        }));
        getRoute(body)
            .then((data) => {
                this.canAddRoute = true
                this.isLoading = false
                if(data.segments && data.segments.length > 0){
                  this.geojsonSource.features[0].geometry.coordinates = data.segments;
                  const midIndex = Math.floor(data.segments.length / 2);
                  const midPoint = data.segments[midIndex];
                  this.center = [midPoint[0], midPoint[1]];
                      this.markers = data.stations.map(station => ({
                        lat: station[0],
                        lon: station[1]
                      }));
                  this.score = data.score
                  this.routeNotFound = false
                  this.mapKey++;
                }else{
                  this.canAddRoute = false
                  this.routeNotFound = true
                }
            })
            .catch((result) => {
                this.canAddRoute = false
                this.isLoading = false
                const { error, toast } = result
                 this.$toast
                    .add({
                      toast
                    })
            })
      }
    },
    complete(event) {
      completePlaces(event.query)
          .then((places) => {
            this.suggestions = places
          })
          .catch((error) => {
            this.$toast.add({
                  severity: 'error',
                  summary: `${errors.internalServerError}`,
                  detail: `${error}`,
                  life: 3000,
                })
          })
    },
    addRoute({ valid, values }){
      this.addRouteIsLoading = true
      const body = {
        segments: {
          segments: this.geojsonSource.features[0].geometry.coordinates,
          stations: this.markers,
        },
        route: {
          start: this.start,
          end: this.end
        }
      }
      addRoute(body)
          .then((response) => {
            this.addRouteIsLoading = false
            this.$toast.add({
              severity: 'success',
              summary: `${success.successfulAddedRoute}`,
              life: 3000,
            })
          })
          .catch( ({ error, toast }) => {
            this.addRouteIsLoading = false
            this.$toast.add(toast)
          })
    }
  },
  mounted() {
    getVehicles()
        .then((data) => {
            this.vehiclesParam = data.vehicles
            this.vehiclesOptions = this.vehiclesParam.map((element, index) => ({
                key: index,
                label: element.model,
                data: element
              }));
        })
   this.drivingStyleOptions = [
  {
    key: 1,
    label: "Sport Driving Style",
    data: 0.5
  },
  {
    key: 2,
    label: "Average Driving Style",
    data: 0.6
  },
  {
    key: 3,
    label: "Eco Driving Style",
    data: 0.9
  }
];
},
}
</script>
<style scoped lang="scss">
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
