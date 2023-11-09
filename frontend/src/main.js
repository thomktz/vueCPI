import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios';
import './styles.css';


axios.defaults.baseURL = process.env.VUE_APP_API_URL;

createApp(App).mount('#app')
