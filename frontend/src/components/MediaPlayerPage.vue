<template>
  <div id="media_container">
    <div id="progress_bar"></div>
    <div class="title">Sample <b>#{{sample_id}}</b></div>
    <div class="subtitle" >{{mediaStore.dataset}} dataset</div>
    <div class='audio-container' @mouseover="addBorder(null)">
      <audio ref="player" controls controlsList="nodownload">
        <source :src="BASE_URL + mediaStore.current_file">
      </audio>
    </div>
    <div id="range_wrapper">
      <div id="range_hint" :class="{'alert_shake': !isValidated}" @mouseover="addBorder(null)">How hard was it to make this decision?</div>
      <div id="range_selector">
        <div class="moving-border top" :style="borderStyle"></div>
        <div
            v-for="(item, index) in items"
            :key="index"
            :class="['item', { 'selected': isSelected(index) }]"
            @click="selectItem(index)"
            @mouseover="addBorder(index)"
        >
          {{ item }}
        </div>
        <div class="moving-border bottom" :style="borderStyle"></div>
      </div>
    </div>

    <div id="selector" @mouseover="addBorder(null)">
      <div id="real_btn" class="btn button-30" @click="choose(1)"><span class="cat">Human</span> speech</div><div id="fake_btn" class="btn button-30" @click="choose(2)"><span class="cat">Synthesized</span> speech</div>
    </div>

    <div id="progress_wrapper">
      <div><b>PROGRESS</b></div>
      <div class="progress_count">{{mediaStore.current_count}}/<b>{{mediaStore.all_count}}</b></div>
      <FancyProgressBar :value="mediaStore.getCountInPercentage"/>
    </div>

    <FancyLoadingOverlay id="foverlay" v-show="loading"/>
  </div>
</template>

<script>

import {computed, onMounted, ref} from "vue";
import {BASE_URL, enterChoice, finalize} from '@/axios';
import { useSessionStore, useMediaStore, useResultStore } from '@/store'
import {useRouter} from "vue-router/dist/vue-router";
import FancyProgressBar from './FancyProgressBar.vue';
import FancyLoadingOverlay from './FancyLoadingOverlay.vue';

export default {
  components: { FancyProgressBar, FancyLoadingOverlay },
  name: "MediaPlayerPage",
  setup() {
    const sample_id = ref('0386')
    const items = ref(["Easy", "Hard"])
    const hoveredItemIndex = ref(null)
    const clickedItemIndex = ref(-1)
    const playCount = ref(0)
    const player = ref(0)
    const isValidated = ref(true)
    const loading = ref(true)
    const router = useRouter()
    const sessionStore = useSessionStore()
    const mediaStore = useMediaStore()
    const resultStore = useResultStore()

    let startTimestamp = -1

    const isSelected = (index) => clickedItemIndex.value === index;

    const selectItem = (index) => {
      clickedItemIndex.value = index;
    };

    function addBorder(index) {
      hoveredItemIndex.value = index;
    }

    const borderStyle = computed(() => {
      if (hoveredItemIndex.value !== null) {
        const item = items.value[hoveredItemIndex.value]; 
        if (item) {
          return {
            width: Math.floor(100/items.value.length) + '%',
            left: Math.floor(100 * hoveredItemIndex.value * (1/items.value.length)) + '%',
          };
        }
      } 
      return {
        width: 0,
      };
      
      
    });

    const reload = (file) => {
      // generate new file name
      const randomNumber = Math.floor(Math.random() * 1001);
      sample_id.value = '0' + randomNumber.toString();

      // reload new file
      mediaStore.nextFile(file)

      // reset playcount, player state, controls
      player.value.pause();
      player.value.currentTime = 0;
      player.value.load();
      player.value.controls = true;
      playCount.value = 0

      // reset timer
      startTimestamp = -1

      // reset difficulty state
      hoveredItemIndex.value = -1
      clickedItemIndex.value = -1
    }

    const choose = async (result) => {
      // validate difficulty
      if( clickedItemIndex.value < 0 || clickedItemIndex.value > items.value.length){
        isValidated.value = false
        return
      } else {
        isValidated.value = true
      }

      // disable button until loading
      if(loading.value){
        return
      } else {
        loading.value = true;
      }

      // stop timer
      const time = (startTimestamp === -1) ? 0: (Date.now() - startTimestamp) / 1000

      const response = await enterChoice(
        mediaStore.current_file, 
        result, 
        clickedItemIndex.value, 
        sessionStore.session_1, 
        sessionStore.session_2, 
        time,
        player.value.currentTime,
        playCount.value,
        player.value.duration
        );

      if(response.data.isEmpty){
        const response2 = await finalize(sessionStore.session_1);
        resultStore.setResult(response2.data.accuracy, response2.data.time)
        await router.push({ name: 'score' })
      } else {
        reload(response.data.nextSample)
      }

    }

    onMounted(() => {
      if(sessionStore.session_1 == '' || sessionStore.session_2 == '' || mediaStore.dataset == ''){
         router.push({ name: '403', params: {reason: "Invalid session"} })
         return
      }

      player.value.addEventListener('loadedmetadata', () => {
        loading.value = false
      })

      player.value.addEventListener('play', () => {
        // start timer if this is the first listen
        if (playCount.value === 0 && startTimestamp === -1){
          startTimestamp = Date.now()
        }

        // increment play count
        if (playCount.value < 2) {
          playCount.value++;
        } else {
          player.value.controls = false;
        }
      });
    });


    return {
      mediaStore,
      sample_id,
      items,
      addBorder,
      borderStyle,
      isSelected,
      selectItem,
      choose,
      player,
      isValidated,
      loading,
      BASE_URL
    }
  }
}
</script>

<style scoped>
@import "./button.css";

.title{
  font-size: 60pt;
  text-transform: uppercase;
  margin-bottom: 10px;
  line-height: 60pt;
  text-align: center;
}
.subtitle{
  text-align: center;
  font-size: 24pt;

  width: 550px;
  background-color: #2c3e50;
  color: white;
  margin: auto;
}

#media_container{
  margin: auto;
  padding-top:20px;
}

.audio-container {
  margin-top: 60px;
  margin-bottom: 60px;

  display: flex;
  justify-content: center;
  align-items: center;
}

audio{
  width: 550px;
}

#selector {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;

  width: 550px;
  margin: auto;
}

#selector .btn{
  width: 45%;
  height: 200px;

  font-size: 20pt;
}

.cat{
  text-transform: uppercase;
  font-weight: bold;
}

.button-30:hover{
  background-color: rgba(227, 227, 227, 1);
}

#range_hint, #range_selector{
  width: 550px;
  margin: auto;
}

#range_hint {
  padding-left: 25px;
  color: #2c3e50;
  font-weight: lighter;
  font-size: 14pt;
  margin-bottom: 10px;
}
#range_selector {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  margin-bottom: 50px;

  position: relative;
}

.item {
  padding: 10px 7px;

  width: 50%;
  text-align: center;

  cursor: pointer;
}

.moving-border {
  position: absolute;
  left: 0;
  width: 0;
  height: 2px;
  background-color: black; /* Change the color as per your preference */
  transition: width 0.3s ease-in-out;
}

.bottom{
  bottom: 0;
}

.top{
  top: 0;
}

.selected {
  background-color: #2c3e50;
  color: white;
  font-weight: bolder;
}

#progress_wrapper {
  position: absolute;
  bottom: 20px;
  right: 50px;
}

.progress_count{
  border-top: 1px solid lightgray;
  border-bottom:1px solid lightgray;
  text-align: center;
}

/* Overlay */
#foverlay {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 3;
  height: 100%;
  width: 100%;
}

/* Form validation */
.alert_shake {
  animation: horizontal-shaking 0.4s 2;
  background-color: #ff7d7d;
  font-weight: bold !important;
  color: white !important;
}

@keyframes horizontal-shaking {
  0% { transform: translateX(0) }
  25% { transform: translateX(10px) }
  50% { transform: translateX(-10px) }
  75% { transform: translateX(10px) }
  100% { transform: translateX(0) }
}
</style>