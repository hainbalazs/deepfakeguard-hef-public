<template>
  <div class="wrapper">
    <input type="range" class="range-style" min="10" max="150" value="50" />
  </div>
</template>

<script>
export default {
  name: "FancySlider"
}
</script>

<style lang="scss" scoped>
*,
*::before,
*::after {
  box-sizing: border-box;
}

$primary: #e0e0e0;

body {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50vh;
  background: $primary;
}


</style>