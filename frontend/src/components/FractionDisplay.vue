<template>
  <div class="container">
    <div class="header-text">Node weight<br>in the whole HICP</div>
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
          {{ formattedFraction }}
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
  </div>
</template>
  
  <script>
  export default {
    name: 'FractionDisplay',
    props: {
      fraction: Number,
      digits: {
        type: Number,
        default: 4 
      },
    },
    computed: {
      radius() {
        return 100 - this.strokeWidth / 2;
      },
      strokeWidth() {
        return 8;
      },
      formattedFraction() {
        // Format the fraction to have up to `this.digits` decimal places without trailing zeroes
        return this.formatFraction(this.fraction, this.digits);
      }
    },
    methods: {
      formatFraction(number, digits) {
        // Convert to fixed, then to float to remove trailing zeroes, then to fixed again with max digits
        return parseFloat(number.toFixed(digits)).toFixed(Math.min(digits, (number.toString().split('.')[1] || '').length));
      }
    }
  };
  </script>
  
  <style scoped>
  .fraction-display {
  position: relative;
  width: 200px; /* adjust as needed */
  height: 200px; /* adjust as needed */
  margin-top: 30px; /* Make space for the absolutely positioned header text */
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
  .container {
  position: relative;
  text-align: center;
}

.header-text {
  position: absolute;
  top: -30px; /* Adjust this value as needed to move the text up */
  left: 50%;
  transform: translateX(-50%);
  font-size: 13px;
}
  </style>
  