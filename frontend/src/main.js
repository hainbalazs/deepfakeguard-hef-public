// main.js
import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import { createPinia } from 'pinia'
import App from './App.vue'; // Import the root component
import VueCookies from 'vue-cookies';

import LandingPage from './components/LandingPage.vue';
import MediaPlayerPage from './components/MediaPlayerPage.vue';
import ResultPage from './components/ResultPage.vue';
import ErrorPage from './components/ErrorPage.vue'

const routes = [
    { path: '/', component: LandingPage },
    {
        name: 'media',
        path: '/media', 
        component: MediaPlayerPage
    },
    {
        name: 'score',
        path: '/score',
        component: ResultPage
    },
    {
        name: '403',
        path: '/403/:reason',
        component: ErrorPage,
        props: true

    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});
const pinia = createPinia()

const app = createApp(App); // Use the root component (App) here

app.use(router);
app.use(VueCookies);
app.use(pinia)

app.mount('#app');
