import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        themes: {
            dark: {
                prominent: '#FFFFFF',
                notable: '#C0C0C0',
                weak: '#1F1F1F',
            }
            ,
            light: {
                prominent: '#000000',
                notable: '#4F4F4F',
                weak: '#F2F2F2',
            }
        }
    }
});
