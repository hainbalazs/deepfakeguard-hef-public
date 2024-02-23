<template>
<div>
  <div id="result_container">
    <div id="accuracy_name">Permission DENIED</div>
    <div id="accuracy_result">403</div>
    <div id="circle"></div>
    <div id="back_btn" @click="back">BACK HOME</div>
  </div>
  <div id="time_taken">Reason: {{reason}}.</div>
</div>

</template>

<script>
import { useRouter } from "vue-router/dist/vue-router";

export default {
  name: "ErrorPage",
  props: {
    reason: {
      type: String,
      required: true,
    },
  },
  setup() {
    const router = useRouter()

    const back = () => {
      router.push({ path: '/'})
    }

    return {
      back
    }

  }
}
</script>

<style scoped>
#result_container{
  width: 800px;
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
  margin-left: 300px;
  line-height: 62pt;
  color: rgb(171, 0, 0);
}

#circle {
  border-radius: 50%;
  width: 400px;
  height: 400px;
  background-color: #D6D6E7;
  position: relative;
  left: 235px;
  top: -285px;
  margin-bottom: -250px;
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