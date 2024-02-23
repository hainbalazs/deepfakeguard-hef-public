import { defineStore } from 'pinia'

export const useSessionStore = defineStore('session', {
    state: () => ({
        session_1: '',
        session_2: ''
    }),
    actions: {
        registerSession(session_1, session_2){
            this.session_1 = session_1
            this.session_2 = session_2
        }, 
        endSession(){
            this.session_1 = ''
            this.session_2 = ''
        }
    }
})

export const useMediaStore = defineStore('media', {
    state: () => ({
        dataset: '',
        current_file: '',
        current_count: '', 
        all_count: '',
    }),
    getters: {
        getCountInPercentage(state){
            return Math.floor((state.current_count / state.all_count) * 100)
        }
    },
    actions: {
        selectDataset(dataset, current_file, current_count, all_count){
            this.dataset = dataset
            this.current_file = current_file
            this.current_count = current_count
            this.all_count = all_count
        }, 
        nextFile(file){
            this.current_file = file
            this.current_count++
        }
    }
})

export const useResultStore = defineStore('result', {
    state: () => ({
        accuracy: -1,
        time: -1
    }),
    actions: {
        setResult(accuracy, time){
            this.accuracy = accuracy
            this.time = time
        }
    }
})