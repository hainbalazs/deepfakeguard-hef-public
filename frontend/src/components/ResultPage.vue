<template>
<div>
  <div id="result_container">
    <div id="accuracy_name">Your accuracy <br> is</div>
    <div id="accuracy_result">{{resultStore.accuracy}}%</div>
    <div id="circle"></div>
    <div id="back_btn" @click="back">BACK HOME</div>
  </div>
  <div id="time_taken">Thinking time throughout the evaluation: {{resultStore.time}} seconds.</div>
</div>

</template>

<script>
import { useRouter } from "vue-router/dist/vue-router";
import { useSessionStore, useResultStore } from '@/store'
import { onMounted } from 'vue';

export default {
  name: "ResultPage",
  setup() {
    const router = useRouter()
    const sessionStore = useSessionStore()
    const resultStore = useResultStore()

    const back = () => {
      sessionStore.endSession()
      router.push({ path: '/'})
    }

    onMounted(() => {
      if(sessionStore.session_1 == '' || sessionStore.session_2 == '' || resultStore.accuracy == -1){
         router.push({ name: '403', params: {reason: "Invalid session"} })
         return
      }
    })

    return {
      back,
      resultStore
    }

  }
}
</script>

<style scoped>
#result_container{
  width: 700px;
  height: 450px;
  margin: 100px auto;
}

#accuracy_name {
  font-size: 72pt;
  font-weight: lighter;
  line-height: 62pt;
}

#accuracy_result {
  font-size: 152pt;
  font-weight: bold;
  margin-left: 100px;
  line-height: 62pt;
}

#circle {
  border-radius: 50%;
  width: 400px;
  height: 400px;
  background-color: #D6D6E7;
  position: relative;
  left: 75px;
  top: -225px;
  margin-bottom: -200px;
  z-index: -1;
}

#back_btn {
  margin-left: auto;
  width: 120px;
  border: 1px solid #2c3e50;
  border-radius: 20px;
  padding: 10px;
  text-align: center;
}

#back_btn:hover{
  cursor: pointer;
  border-width: 2px;
  transform: translateX(1px) translateY(-1px);
}


#time_taken {
  position:absolute;
  left: 15px;
  bottom: 5px;
  color: grey;
  font-weight: 300;
}
</style>