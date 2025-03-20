<script>
import Menubar from "primevue/menubar";
import * as backend from "@/backend/backend.js";
import {errors} from "@/constants/constants.js";
import {verify} from "@/backend/backend.js";
import {useAuthStore} from "@/stores/auth.js";
export default {
  name: "Navbar",
  data(){
    return {
      items: [
           {
                label: 'Routes',
                icon: 'pi pi-map',
                command: () => {
                  this.$router.push("/users/routes")
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
      console.log(authStore.authToken)
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
                  this.items[1].visible = true;
                })
                .catch(() => {
                  this.items[1].visible = false;
                });
            } else {
              this.items[1].visible = false;
            }
          },
        },
    },
  mounted() {
    this.authToken;
  },
}
</script>

<template>
    <div class="card">
        <Menubar :model="items" />
    </div>
</template>
