<template>
  <v-container class="pa-0">
    <v-card flat width="21.6cm" height="27.9cm" class="mx-auto d-flex flex-column" tile outlined>
      <v-card-title class="pa-0 align-end white--text pl-7"
                    style="background:linear-gradient(60deg, #DA22FF 20%, #9733EE 80%)">
        <div class="mt-2" style="width:150px;position:absolute;top:0;left:28px">
          <h4 class="my-0 text-center">Juan Fernando</h4>
          <h5 class="my-0 text-center">Dederlé Baena</h5>
        </div>
        <v-img height="150" max-width="150" class="rounded-circle elevation-5"
               src="@/assets/profile.jpeg" style="transform:translateY(50%)">
        </v-img>
        <div class="ma-2 grow font-italic text-center text-uppercase align-self-center"
             style="text-shadow:2px 2px 0 #2f2f2f">
          Full stack web developer
        </div>
        <div class="subtitle-2 ma-2">
          <v-avatar color="white" class="ma-2" size="29">
            <v-icon color="blue" large>mdi-home-circle-outline</v-icon>
          </v-avatar>
          Medellín - Colombia<br>
          <v-avatar color="white" class="ma-2" size="29">
            <v-icon color="green" large>mdi-whatsapp</v-icon>
          </v-avatar>
          (+57) 311 332 9905<br>
          <v-avatar color="white" class="ma-2" size="29">
            <v-icon color="red" large>mdi-google</v-icon>
          </v-avatar>
          jfdeder@gmail.com
        </div>
      </v-card-title>
      <v-card-text class="pa-0 d-flex grow">
        <div class="pa-4 weak" :style="'border-right: 1px solid' + '#e0e0e0' + '!important'">
          <h3 class="text-center" style="margin-top:70px">Skills</h3>
          <v-list class="mb-4" subheader outlined>
            <v-subheader style="height: 30px">Backend</v-subheader>
            <v-list-item dense>
              <v-list-item-avatar tile size="20">
                <v-icon color="#ffcb6b">mdi-language-python</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>Python</v-list-item-title>
              </v-list-item-content>
            </v-list-item>

            <v-list-item dense>
              <v-list-item-avatar size="20" class="font-weight-black" style="color:white;background:#0c4b33;">
                dj
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>Django</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-list class="mb-4" subheader outlined>
            <v-subheader style="height: 30px">Frontend</v-subheader>
            <v-list-item dense>
              <v-list-item-avatar tile size="20">
                <v-icon color="#efd81d">mdi-language-javascript</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>Javascript</v-list-item-title>
              </v-list-item-content>
            </v-list-item>

            <v-list-item dense>
              <v-list-item-avatar tile size="20">
                <v-icon color="#563d7c">mdi-bootstrap</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>Bootstrap</v-list-item-title>
              </v-list-item-content>
            </v-list-item>

            <v-list-item dense>
              <v-list-item-avatar tile size="20">
                <v-icon color="#41b883">mdi-vuejs</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>Vue</v-list-item-title>
                <v-list-item-subtitle>Vuex</v-list-item-subtitle>
                <v-list-item-subtitle>Vue-Router</v-list-item-subtitle>
                <v-list-item-subtitle>Vue-Cli</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-list-item dense>
              <v-list-item-avatar tile size="20">
                <v-icon color="#7bc6ff">mdi-vuetify</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>Vuetify</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-list class="mb-4" subheader outlined>
            <v-subheader style="height: 30px">Frontend & Backend</v-subheader>
            <v-list-item dense>
              <v-list-item-avatar tile size="20">
                <v-icon color="#e535ab">mdi-graphql</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>GraphQL</v-list-item-title>
                <v-list-item-subtitle>Graphene-Django</v-list-item-subtitle>
                <v-list-item-subtitle>Vue-Apollo</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-list class="mb-4" subheader outlined>
            <v-subheader style="height: 30px">Systems</v-subheader>
            <v-list-item dense>
              <v-list-item-avatar tile size="20">
                <v-icon color="#4285f5">mdi-google-cloud</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>Google cloud</v-list-item-title>
                <v-list-item-subtitle>PubSub</v-list-item-subtitle>
                <v-list-item-subtitle>GKE</v-list-item-subtitle>
                <v-list-item-subtitle>Compute Engine</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-list-item dense>
              <v-list-item-avatar tile size="20">
                <v-icon color="#2496ed">mdi-docker</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>Docker</v-list-item-title>
              </v-list-item-content>
            </v-list-item>

            <v-list-item dense>
              <v-list-item-avatar tile size="20">
                <v-icon color="#326de6">mdi-kubernetes</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>Kubernetes</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </div>
        <div class="d-flex flex-column" style="justify-content: space-evenly;">
          <v-alert icon="mdi-account-tie" border="left" color="#9733EE" colored-border
                   elevation="1" dense class="mb-0 mx-11">
            <h4 class="mt-1 mb-4">Profile</h4>
            <p class="caption font-weight-light text-justify">
              Experienced web developer, adept with software development stages such as; design, automated testing,
              debugging, deployment and maintenance. Proficient in REST/GRAPHQL API development, responsive web UI
              design and creation, and integrating both API and UI through multi or single page application designs.
              Bringing forth knowledge in development and deployment environments configuration under the concepts of
              containers, and clusters for deployment infrastructures, complementing with knowledge in event-driven and
              microservice architecture patterns. Adroit at integrating secure practices against OWASP's most common
              security vulnerabilities in both development and deployment scenarios.
            </p>
          </v-alert>

          <v-alert icon="mdi-briefcase-variant" border="left" color="#9733EE" colored-border
                   elevation="1" dense class="mb-0 mx-11">
            <h4 class="my-1">Experience</h4>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title class="subtitle-2">
                  Analyst/Developer at <i>Pagoagil</i> payment gateway.
                </v-list-item-title>
                <v-list-item-subtitle class="caption">November 2019 - Now</v-list-item-subtitle>
                <ul class="caption">
                  <li>
                    Development and testing new API exposing transaction validating and registering functionality for
                    third party companies to consume
                  </li>
                  <li>
                    Development of transaction authorization system, based of consulted data from credit bureaus and
                    fraud detection metrics
                  </li>
                  <li>
                    Deployment in Google Cloud Platform, with an asynchronous event-driven and microservice architecture
                    through cluster setups
                  </li>
                  <li>
                    Secure development and deployment practices, such as encryption, secure protocols and
                    authentication/authorization systems
                  </li>
                </ul>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title class="subtitle-2">
                  Backend developer - Orders and shops catalogs web site.
                </v-list-item-title>
                <v-list-item-subtitle class="caption">May 2020 - July 2020</v-list-item-subtitle>
                <ul class="caption">
                  <li>
                    Backend REST API TDD featuring; authentication, orders, search engine, shops/products
                    and admin panel modules
                  </li>
                  <li>
                    Final web site deployment on linux virtual machine with GCP's Compute Engine service
                  </li>
                </ul>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title class="subtitle-2">
                  Full stack web developer - Tourism agency web site.
                </v-list-item-title>
                <v-list-item-subtitle class="caption">July 2016 - October 2016</v-list-item-subtitle>
                <ul class="caption">
                  <li>
                    Backend and responsive frontend UI, featuring travel planes and products catalog. Deployed
                    on BlueHost web hosting
                  </li>
                </ul>
              </v-list-item-content>
            </v-list-item>
          </v-alert>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data: () => ({})
}
</script>
