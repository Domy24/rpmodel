<template>
    <div class="card">
        <DataTable v-model:selection="selectedProduct" :value="products" dataKey="id" :metaKeySelection="false"
                @rowClick="onRowClick" tableStyle="min-width: 50rem" :rowHover="true">
            <Column field="start" header="Punto di partenza"></Column>
            <Column field="end" header="Punto di destinazione"></Column>
            <Column field="id" header="ID"></Column>
        </DataTable>
        <Toast/>
    </div>
    <div>
    <UserRouteDetailComponent v-if="routeDetails.coordinates.length > 0" :key="routeDetails.id" :coordinates="routeDetails.coordinates" :markers="routeDetails.markers"/>
  </div>
</template>


<script>
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';   // optional
import Row from 'primevue/row';
import {getUserRoutes, getDetailUserRoute} from "@/backend/backend.js";
import UserRouteDetailComponent from "@/components/UserRouteDetailComponent.vue";
export default {
  name: "UserRoutesComponent",
  components: {
    UserRouteDetailComponent,
    DataTable,
    Column,
    ColumnGroup,
    Row
  },
  data() {
        return {
            products: [],
            selectedProduct: null,
            routeDetails: {
              coordinates : [],
              id: null,
              markers: []
            }
        };
    },
  methods: {
        onRowClick(event) {
            getDetailUserRoute(event.data.id)
                .then((response) => {
                    this.routeDetails.coordinates = response.route.segments
                    this.routeDetails.markers = response.route.stations
                    this.routeDetails.id = event.data.id
                })
                .catch((result) => {
                  const { error, toast } = result
                  this.$toast.add(toast)
                })
        },
    },
  mounted() {
    getUserRoutes()
        .then((data) => {
          if(data.routes.length > 0){
            this.products = data.routes
          }
        })
        .catch((result) => {
          const { error, toast } = result
          this.$toast.add(toast)
        })
  }
}
</script>

<style scoped>

</style>
