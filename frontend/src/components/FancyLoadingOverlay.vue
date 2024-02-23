<template>
    <div class="overlay">
        <span class="loader"></span>
    </div>
</template>

<script>
export default {
  name: "FancyLoadingOverlay"

}
</script>

<style scoped>
.overlay{
    height: 100%;
    width: 100%;
    background-color: rgba(211, 211, 211, 0.25);
    backdrop-filter: blur(5px);

    display: flex;
    align-items: center;
    justify-content: center;
}

.loader {
    animation: rotate 1s infinite;
    height: 50px;
    width: 50px;
  }

  .loader:before,
  .loader:after {
    border-radius: 50%;
    content: "";
    display: block;
    height: 20px;
    width: 20px;
  }
  .loader:before {
    animation: ball1 1s infinite;
    background-color: #0ab8e7;
    box-shadow: 30px 0 0 #e86800;
    margin-bottom: 10px;
  }
  .loader:after {
    animation: ball2 1s infinite;
    background-color: #e86800;
    box-shadow: 30px 0 0 #0ab8e7;
  }

  @keyframes rotate {
    0% { transform: rotate(0deg) scale(0.8) }
    50% { transform: rotate(360deg) scale(1.2) }
    100% { transform: rotate(720deg) scale(0.8) }
  }

  @keyframes ball1 {
    0% {
      box-shadow: 30px 0 0 #e86800;
    }
    50% {
      box-shadow: 0 0 0 #e86800;
      margin-bottom: 0;
      transform: translate(15px, 15px);
    }
    100% {
      box-shadow: 30px 0 0 #e86800;
      margin-bottom: 10px;
    }
  }

  @keyframes ball2 {
    0% {
      box-shadow: 30px 0 0 #0ab8e7;
    }
    50% {
      box-shadow: 0 0 0 #0ab8e7;
      margin-top: -20px;
      transform: translate(15px, 15px);
    }
    100% {
      box-shadow: 30px 0 0 #0ab8e7;
      margin-top: 0;
    }
  }
  
</style>