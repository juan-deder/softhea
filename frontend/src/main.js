import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import {createHttpLink} from "apollo-link-http";
import {InMemoryCache} from "apollo-cache-inmemory";
import {ApolloClient} from "apollo-client";
import {ApolloLink, concat} from "apollo-link";
import VueApollo, {ApolloProvider} from "vue-apollo";
import moment from 'moment'

Vue.config.productionTip = false

window.Cookie = require('js-cookie')

window.axios = require('axios')
window.axios.defaults.withCredentials = true

Vue.prototype.moment = moment
Vue.use(moment);

Vue.use(VueApollo)

function bootstrap() {
    let httpLink = new createHttpLink({
        uri: 'http://127.0.0.1:8000/graphql',
        credentials: 'include'
    })
    let csrfMiddleware = new ApolloLink((operation, forward) => {
        operation.setContext(({headers = {}}) => ({
            headers: {
                ...headers,
                'X-CSRFToken': Cookie.get('csrftoken')
            }
        }))
        return forward(operation)
    })
    let apolloClient = new ApolloClient({
        link: concat(csrfMiddleware, httpLink),
        cache: new InMemoryCache()
    })
    let apolloProvider = new ApolloProvider({
        defaultClient: apolloClient
    })

    new Vue({
        router,
        store,
        vuetify,
        apolloProvider,
        render: function (h) {
            return h(App)
        }
    }).$mount('#app')
}

if (Cookie.get('csrftoken') === undefined)
    axios.get('http://127.0.0.1:8000/csrf-cookie').then(() => bootstrap())
else
    bootstrap()
