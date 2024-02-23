<template>
  <div id="landing_container">
    <div class="title">
      <h1>Voice cloning</h1>
      <h2>Human Evaluation</h2>
    </div>

      <div class="fade-out" v-show="showGreetings">
        <div class="float">
          <div class="name_title">Candidate's name: </div>
          <input type="text" name="name" v-model="name" @input="handleInputChange" :class="{ 'alert_shake': !isValidated }">
          <button class="button-30" @click="start">START</button>
        </div>
        <div id="start_btn"></div>
      </div>

      <div id="section2" class="fade-in" v-show="!showGreetings">
        <div id="section21">
        <div class="greetings">
          <div class="name_title">Hello, <b><i>{{name}}</i></b> !</div>
          <div class="sub_title">Choose how do you want to proceed?</div>
        </div>
        <div id="btn_holder">
          <div class="button-30 stage_select" :class="{ 'disabled-button': continueIsDisabled }" @click="continueSession">
            <div class="btn_text">Continue</div>
            <div class="btn_sub"> previous test</div>
          </div>
          <div class="button-30 stage_select" @click="selectList">
            <div class="btn_text">Restart</div>
            <div class="btn_sub">a new evaluation</div>
          </div>
        </div>
        </div>
        <div id="section22" v-show="showList">

          <ul>
            <li v-for="project in projects" v-bind:key="project.name" @click="startSession(project.name)">
              {{ project.name }}
            </li>
          </ul>

          <div v-if="false" id="sample_slider">
            <div id="sr_wrapper">
              <div class="sample_title">Select the sample rate</div>
              <input type="number" v-model="textFieldValue" class="sample_value">
            </div>
            <input type="range" class="range-style" min="100" max="100" v-model="sliderValue"/>
          </div>
        </div>
      </div>



  </div>
</template>

<script>
import {computed, ref} from 'vue';
import { useRouter } from 'vue-router'
import {login, listDatasets, startNewSession, loadPreviousSession} from '@/axios';
import { useSessionStore, useMediaStore } from '@/store'

export default {
  name: "LandingPage",
  setup() {
    // Create a reactive reference to the input value
    const name = ref(''); // TODO: remove
    const showGreetings = ref(true);
    const showList = ref(false);
    const projects = ref([{ name: 'HiGAN' }, { name: 'VITS' }, { name: 'WaveGlow' }, { name: 'YourTTS' }])
    const sliderValue = ref(100);
    const textFieldValue = ref('100');
    const continueIsDisabled = ref('True')
    const isValidated = ref(true)
    const router = useRouter()
    const sessionStore = useSessionStore()
    const mediaStore = useMediaStore()

    // Function to handle input changes
    const handleInputChange = (event) => {
      name.value = event.target.value;
    };

    const start = async () => {
      if(name.value === ''){
        isValidated.value = false
        return
      } else {
        isValidated.value = true
      }

      const response = await login(name.value);
      continueIsDisabled.value = !response.data.result
      showGreetings.value = false;
    };

    const selectList = async () => {
      const response = await listDatasets(name);
      projects.value = response.data.datasets.map((datasetName) => ({ name: datasetName }));
      showList.value = true;
    };

    const startSession = async (dataset) => {
      const response = await startNewSession(name.value, dataset, sliderValue.value);

      if (response.data.current_count != 0){
        console.log("Error: Current count is not zero at the start of a new session")
      }

      if (response.data.all_count != sliderValue.value * 2){
        console.log("Warning: The length of the provided sample set is not equal to the value that the user specified. This is only the expected behaviour if the dataset does not have sufficient length.")
      }
      
      sessionStore.registerSession(response.data.session_1, response.data.session_2)
      mediaStore.selectDataset(dataset, response.data.nextSample, response.data.current_count, response.data.all_count)
      router.push({ name: 'media'})
    }

    const continueSession = async () => {
      const response = await loadPreviousSession(name.value);
      sessionStore.registerSession(response.data.session_1, response.data.session_2)
      mediaStore.selectDataset(response.data.dataset, response.data.nextSample, response.data.current_count, response.data.all_count)
      router.push({ name: 'media' });
    }

    const syncedSliderValue = computed({
      get: () => Number(sliderValue.value),
      set: (newValue) => {
        sliderValue.value = newValue;
        textFieldValue.value = String(newValue);
      },
    });

    return {
      name,
      showGreetings,
      showList,
      projects,
      continueIsDisabled,
      handleInputChange,
      start,
      startSession,
      continueSession,
      selectList,
      sliderValue: syncedSliderValue,
      textFieldValue: syncedSliderValue,
      isValidated,
    };
  },
};
</script>


<style scoped>
@import "./button.css";

#landing_container{
  width: 70%;
  margin: auto;
}

.title{
  text-align: center;
  margin-top: 60px;
  margin-bottom: 120px;
  font-weight: bolder;
}

.sub_title{
  font-size: 18pt;
}

h1 {
  font-size: 72pt;
  text-transform: uppercase;
  margin: 0;
  line-height: 72pt;
}

h2 {
  font-size: 50pt;
  margin:0;
  padding:0;
  line-height: 50pt;
}

.name_title {
  font-size: 40pt;
  min-width: 45%;  
}

.float{
  display: flex;
  flex-direction: row;
  width: 100%;
  justify-content: space-between;
  align-items: center;
}

input {
  width: 40%;
  border: 0;
  border-bottom: 2px solid black;
  font-size: 40pt;
}

input:hover{
  border-color: #42b983;
}

input:focus, textarea:focus, select:focus{
  outline: none;
}

#start_btn {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.btn_text {
  font-size: 18pt;
  font-weight: bold;
}


.stage_select{
  padding: 20px;
  margin-bottom: 10px;
  margin-right: 20px;
  width: 200px;
  height: 60px;
}

#section21{
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-bottom: 30px;
}

.greetings{
  align-self: flex-start;
}

#btn_holder{
  margin: auto;
  display: flex;
  flex-direction: row;
}

ul{
  padding: 0;
  margin: 0;

  width: 100%;
}

li {
  list-style-type: none;
  background-color: #444444;
  margin: 0 0 10px 0;

  padding: 10px 10px 10px 20px;
  color: white;

  display: flex;
  flex-direction: row;
}

li:hover{
  background-color: #000000;
}

#sample_slider {
  display: flex;
  flex-direction: column;

  width: 20%;
  margin-left: 25px;
  padding-left: 15px;
}

#sr_wrapper{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

#sample_slider input{
  border: none;
}

input.sample_value {
  font-size: 24pt;
  width: 60pt;
  margin-bottom: 10px;
  align-self: center;
  text-align: center;
}

#section22{
  display: flex;
  flex-direction: row;

}

.sample_title{
  margin-bottom: 20px;
  padding-left: 15px;
  font-size: 15pt;
}

#sample_slider.range-style, input.range-style{
  width: 90%;
}

.disabled-button {
  cursor: not-allowed;
  opacity: 0.6;

}
</style>

<style lang="scss">
$primary: #e0e0e0;
input[type='range'] {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  &:focus {
    outline: none;
  }
  &::-webkit-slider-thumb {
    -webkit-appearance: none;
  }
  &::-moz-range-thumb {
    border: none;
  }
}

.range-style {
  height: 20px;
  padding: 10px;
  background: $primary;
  border-radius: 10px;
  box-shadow: -2px -2px 8px white, 2px 2px 8px rgba(black, 0.5);

  @mixin track-style {
    display: flex;
    align-items: center;
    height: 20px;
    border-radius: 10px;
    box-shadow: inset -2px -2px 8px white, inset 2px 2px 8px rgba(black, 0.5);
  }

  @mixin thumb-style {
    position: relative;
    top: -18%;
    width: 30px;
    height: 30px;
    background-color: $primary;
    background-image: linear-gradient(-45deg, rgba(white, 0.8), transparent);
    border-radius: 50%;
    box-shadow: -1px -1px 2px white, 1px 1px 2px rgba(black, 0.3);
  }
  &::-webkit-slider-runnable-track {
    @include track-style;
  }
  &::-webkit-slider-thumb {
    @include thumb-style;
  }
  &::-moz-range-track {
    @include track-style;
  }
  &::-moz-range-thumb {
    @include thumb-style;
  }
}

.alert_shake {
  animation: horizontal-shaking 0.5s 2;
  border-bottom: 2px solid red !important;
}

@keyframes horizontal-shaking {
  0% { transform: translateX(0) }
  25% { transform: translateX(20px) }
  50% { transform: translateX(-20px) }
  75% { transform: translateX(20px) }
  100% { transform: translateX(0) }
}
</style>