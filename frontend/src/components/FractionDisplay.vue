<template>
    <div class="fraction-display">
      <svg viewBox="0 0 200 200" class="fraction-circle">
        <circle
          :r="radius"
          cx="100"
          cy="100"
          :stroke-width="strokeWidth"
          fill="transparent"
          stroke="#293a5e"
        />
  
        <text
          class="fraction-text"
          text-anchor="middle"
          x="100"
          y="100"
          dy=".3em"
        >
          {{ fraction.toFixed(digits) }}
        </text>
  
        <text
          class="fraction-text denominator"
          text-anchor="middle"
          x="100"
          y="130"
          dy=".3em"
        >
          /1000
        </text>
      </svg>
    </div>
  </template>
  
  <script>
  export default {
    name: 'FractionDisplay',
    props: {
      fraction: Number,
      digits: Number,

    },
    computed: {
      radius() {
        return 100 - this.strokeWidth / 2;
      },
      strokeWidth() {
        return 8;
      },
    },
  };
  </script>
  
  <style scoped>
  .fraction-display {
    position: relative;
    width: 200px; /* adjust as needed */
    height: 200px; /* adjust as needed */
  }
  
  .fraction-circle {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
  
  .fraction-text {
    font-size: 20px;
    fill: white;
    font-family: 'Roboto', sans-serif;
    font-weight: 350;
    letter-spacing: 1px;
  }
  
  .fraction-text.denominator {
    font-size: 15px;
    font-weight: 300;
  }
  </style>
  