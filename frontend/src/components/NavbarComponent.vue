<template>
    <div class="card">
        <Menubar :model="items" />
    </div>
</template>

<script>
import Menubar from "primevue/menubar";
import * as backend from "@/backend/backend.js";
import {errors, pathsName} from "@/constants/constants.js";
import {verify} from "@/backend/backend.js";
import {useAuthStore} from "@/stores/auth.js";
export default {
  name: "Navbar",
  components: Menubar,
  data(){
    return {
      items: [
           {
                label: 'Routes',
                icon: 'pi pi-bars',
                visible: this.authToken,
                command: () => {
                  this.$router.push({name: pathsName.userRoutesView})
                }
            },
              {
                label: 'EVRP',
                icon: 'pi pi-map',
                command: () => {
                  this.$router.push({ name: pathsName.routeView})
                }
            },
           {
                label: 'Profile',
                icon: 'pi pi-user',
                visible: this.authToken,
                items: [
                  {
                    label: "log Out",
                    icon: "pi pi-sign-out",
                    command: () => {
                      backend.logout()
                          .then((response) => {
                            this.$router.push({ name: response.redirect })
                          })
                          .catch((error) => {
                            const toast = error.toast
                            this.$toast.add({ toast })
                      })
                }
                  }
                 ]

            },
      ]
    }
  },
    computed: {
    authToken() {
      const authStore = useAuthStore();
      return authStore.authToken !== null;
    },
  },
      watch: {
        authToken: {
          immediate: true,
          handler(newToken) {
            if (newToken) {
              verify(newToken)
                .then(() => {
                  this.items[2].visible = true;
                  this.items[0].visible = true;
                })
                .catch(() => {
                  this.items[2].visible = false;
                  this.items[0].visible = false;
                });
            } else {
              this.items[2].visible = false;
              this.items[0].visible = false;
            }
          },
        },
    },
  mounted() {
    if (this.authToken) {
        verify(this.authToken)
            .then(() => {
                this.items[2].visible = true;
                this.items[0].visible = true;
            })
            .catch(() => {
                this.items[2].visible = false;
                this.items[0].visible = false;
            });
    } else {
        this.items[2].visible = false;
        this.items[0].visible = false;
    }
}

}
</script>
