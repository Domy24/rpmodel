<template>
  <div class="flex items-center justify-center min-h-screen">
    <Card style="width: 800px; height: 500px;" class="bg-cover bg-center relative bottom-12 ">
      <template #content>
        <img alt="user header" src="https://cdn.prod.website-files.com/637d6390b70424b49c14ff1e/63e08e178b6096f1b04f4229_route-planning-vs-route-optimization-hero.webp" />
      </template>
      <template #footer>
        <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2">
          <Button label="Prova ora!" icon="pi pi-map" class="w-full top-2" @click="redirectOnRoutePage()"/>
        </div>
      </template>
    </Card>
  </div>
</template>

<script>
import Card from 'primevue/card';
import Button from 'primevue/button';
import { pathsName } from "@/constants/constants.js"
import {useAuthStore} from "@/stores/auth.js";


export default {
  name: 'BackgroundPanel',
  components: {
    Card,
    Button
  },
  data() {
    return {
      imageUrl: 'https://it.freepik.com/foto-gratuito/allungamento-della-donna-piu-grande-del-colpo-pieno_38169980.htm#from_element=category_discover&from_view=category'
    };
  },
  methods: {
    redirectOnRoutePage () {
      this.$router.push({name: pathsName.routeView})
    }
  }
};
</script>

<style scoped>

.bg-cover {
  background-size: cover;
  background-position: center;
}
</style>
