<template>
  <svg>
    <circle
      :r="pieChart.getInnerRadius() - 8"
      cx="100"
      cy="100"
      fill="#293a5e"
    />
    <image :href="getIcon()" x="75" y="50" height="30px" width="50px"/>
    <text
      :style="{fontSize: '20px', fill:'white', fontFamily: 'Roboto', fontWeight: '350', letterSpacing: '1px'}"
      text-anchor="middle"
      x="100"
      y="110"
    >
      {{ weight }}
    </text>
    <line 
      x1="80"
      y1="120"
      x2="120"
      y2="120"
      style="stroke:rgb(255,255,255);stroke-width:1"
    />
    <text
      :style="{fontSize: '15px', fill:'white', fontFamily: 'Roboto', fontWeight: '300', letterSpacing: '1px'}"
      text-anchor="middle"
      x="100"
      y="140" 
    >
      1000
    </text>
  </svg>
</template>

<script>
import itemIcon from '@/assets/item_icon.svg';

export default {
  props: {
    pieChart: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      weight: this.pieChart.getAllSeries()[0].getVisiblePoints()[0].data.weight,
      code: this.pieChart.getAllSeries()[0].getVisiblePoints()[0].data.code.toLowerCase(),
    }
  },
  methods: {
    getIcon() {
      console.log("CODEEE, ", this.code);
      if (this.code === 'ea19') {
        this.code = 'eu';
      }
      
      if (this.code === 'item') {
        return itemIcon;
      } else {
        return `https://flagcdn.com/${this.code}.svg`;
      }
    },
  }
  
};
</script>
