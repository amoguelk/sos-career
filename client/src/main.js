import { createApp } from "vue";

// Pinia
import { createPinia } from "pinia";

const pinia = createPinia();

// Vuetify
import "vuetify/styles";
import { createVuetify } from "vuetify";
import colors from "vuetify/util/colors";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import "@mdi/font/css/materialdesignicons.css";

const baseColor = colors.blueGrey;
const vuetify = createVuetify({
  components,
  directives,
  theme: {
    themes: {
      light: {
        dark: false,
        colors: {
          primary: baseColor.darken1,
          secondary: baseColor.darken4,
          background: colors.shades.white,
          surface: baseColor.lighten5,
        },
      },
    },
  },
});

// Components
import App from "./App.vue";
import router from "./router";

const app = createApp(App);

app.use(router);
app.use(vuetify);
app.use(pinia);

app.mount("#app");
