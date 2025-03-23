<template>
  <div class="map-container">
    <mgl-map
        :key="key"
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
</template>

<script>
import {
  MglGeoJsonSource,
  MglLineLayer,
  MglMap,
  MglNavigationControl
} from "@indoorequal/vue-maplibre-gl";
import {number} from "yup";

export default {
  components: {
    MglMap,
    MglLineLayer,
    MglNavigationControl,
    MglGeoJsonSource
  },
  name: "UserRouteDetailComponent",
  props: {
  coordinates: {
    type: Array,
    required: true,
  },
  key: {
    type: number,
    required: true
  },
  markers: {
    type: Array,
    required: true,
  }
},
  data () {
    return {
        style: 'https://api.maptiler.com/maps/streets-v2/style.json?key=ssYZIhglJGSf9GYsHiOO',
        zoom: 6,
        geojsonSource: {
        type: "FeatureCollection",
        features: [
          {
            type: "Feature",
            properties: {},
            geometry: {
              type: "LineString",
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
      markers: [],
      center:  [ 12.481633, 41.894431 ],
    }
  },
  watch: {
    coordinates: {
      immediate: true,
      handler(newCoordinates) {
        this.geojsonSource.features[0].geometry.coordinates = newCoordinates;
      },
    },
    markers: {
      immediate: true,
      handler(newMarkers) {
        this.markers = newMarkers;
      },
    },
  },
}
</script>

<style>

.map-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

</style>