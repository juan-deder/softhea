<template>
  <v-app>
    <v-app-bar app clipped-left short :collapse="collapsed" :hide-on-scroll="!collapsed"
               :prominent="!collapsed" :color="collapsed ? 'transparent' : ''" scroll-threshold="0"
               :style="!collapsed || 'background:linear-gradient(60deg, #DA22FF 20%, #9733EE 80%)'">

      <v-app-bar-nav-icon @click="collapsed = !collapsed" :dark="collapsed" light>
      </v-app-bar-nav-icon>

      <template v-slot:img="{ props }">
        <v-img class="fill-height" src="./assets/water_drop.jpg" v-if="!collapsed">
          <div class="fill-height"
               style="background:linear-gradient(135deg, white 25%, transparent 40%), linear-gradient(175deg, transparent 70%, black 90%)">
          </div>
        </v-img>
      </template>

      <template v-if="!collapsed">
        <v-img max-width="250" position="left" height="100%" contain
               src="./assets/logo.png">
        </v-img>

        <v-spacer></v-spacer>

        <v-btn @click="dark = !dark" icon color="amber accent-4">
          <v-icon>{{ themeIcon }}</v-icon>
        </v-btn>
        <v-btn icon dark>
          <v-icon>mdi-account</v-icon>
        </v-btn>
      </template>

      <template v-slot:extension>
        <v-tabs color="purple lighten-1" slider-size="3">
          <v-tab to="/" class="grey--text text--darken-2">Home</v-tab>
          <v-tab class="grey--text text--darken-2">Solutions</v-tab>
          <v-spacer></v-spacer>
          <v-tab to="/blog" class="white--text">Blog</v-tab>
          <v-tab class="white--text">Contact</v-tab>
          <v-tab to="/about" class="white--text">About</v-tab>
        </v-tabs>
      </template>
    </v-app-bar>

    <v-main :class="{ 'pt-0': collapsed }">
      <router-view></router-view>
    </v-main>

<!--    <v-footer app absolute>-->
<!--      Footer-->
<!--    </v-footer>-->
  </v-app>
</template>

<script>
export default {
  name: 'App',

  data: () => ({
    preferences: JSON.parse(Cookie.get('preferences') || '{}'),
    dark: null,
    themeIcon: null,

    collapsed: false
  }),

  created() {
    this.themeIcon = this.getIcon()

    this.dark = this.preferences.dark
    console.log(this.$vuetify)
  },

  methods: {
    getIcon() {
      return this.dark ? 'mdi-brightness-7' : 'mdi-brightness-5';
    },

    changePreference(key, value) {
      this.preferences[key] = value
      Cookie.set('preferences', JSON.stringify(this.preferences))
    }
  },

  watch: {
    async dark() {
      this.themeIcon = 'mdi-brightness-4'
      await new Promise(r => setTimeout(r, 100))
      this.themeIcon = this.getIcon()
      this.$vuetify.theme.dark = this.dark

      this.changePreference('dark', this.dark)
    }
  },
};
</script>
