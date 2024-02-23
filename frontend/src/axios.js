// api.js
import axios from 'axios';

export const BASE_URL = '<BACKEND_URL>'; // Replace this with your Django server URL

const api = axios.create({
    baseURL: BASE_URL,
});
api.defaults.xsrfHeaderName = 'x-csrftoken'
api.defaults.xsrfCookieName = 'csrftoken'
api.defaults.withCredentials = false

export const init = () => 
    api.get('init/');
export const login = (name) => 
    api.get('login/', { params: {name} });
export const listDatasets = () => 
    api.get('list_datasets/');
export const startNewSession = (name, dataset, sampleSize) => 
    api.get('start_new_session/', { params: { name, dataset, sampleSize } });
export const loadPreviousSession = (name) => 
    api.get('load_previous_session/', { params: { name } });
export const enterChoice = (filename, result, difficulty, session_1, session_2, time, player_position, playcount, audio_length) => 
    api.get('enter_choice/', { params: {filename, result, difficulty, session_1, session_2, time, player_position, playcount, audio_length}});
export const finalize = (session_1) => 
    api.get('finalize/', {params: {session_1}});