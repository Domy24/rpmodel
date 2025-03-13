<script>
import Menubar from "primevue/menubar";
export default {
  name: "Navbar",
  data(){
    return {
      items: [
           {
                label: 'Routes',
                icon: 'pi pi-map',
                command: () => {
                  this.$router.push("/routes")
                }
            },
           {
                label: 'Profile',
                icon: 'pi pi-user'
            },
      ]
    }
  }
}
</script>

<template>
    <div class="card">
        <Menubar :model="items" />
    </div>
</template>
