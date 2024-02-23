<template>
  <router-view></router-view>
</template>

<script>
export default {
  name: 'App',
  components: {
  }
}
</script>

<style>

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  /*margin-top: 60px;*/
  /*transform: scale(0.9);*/
}

@font-face {
  font-family: 'Avenir';
  src: url('../fonts/AvenirLight.ttf') format('truetype');
  font-weight: 300; /* Light */
  font-style: normal;
}

@font-face {
  font-family: 'Avenir';
  src: url('../fonts/AvenirRegular.ttf') format('truetype');
  font-weight: 400; /* Regular */
  font-style: normal;
}

@font-face {
  font-family: 'Avenir';
  src: url('../fonts/AvenirBlack.ttf') format('truetype');
  font-weight: 700; /* Bold */
  font-style: normal;
}
</style>
