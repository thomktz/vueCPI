<template>
  <highcharts :options="chartOptions" ref="chart"></highcharts>
</template>


<script>
import axios from 'axios';
import { timeParse } from 'd3';
import { Chart } from 'highcharts-vue'

export default {
  name: 'SingleTimeSeries',
  components: {
    highcharts: Chart
  },
  props: {
    node: String,
    country: String,
  },
  data() {
    return {
      chartOptions: {}
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get(`/data/${this.country}/${this.node}`);
        this.setChartOptions(response.data);
      } catch (error) {
        console.error(error);
      }
    },
    setChartOptions(data) {
      const parseTime = timeParse("%Y-%m-%d");

      data.forEach((d) => {
        d.date = parseTime(d.date).getTime();  // Convert date to timestamp
        d.value = +d.value;
      });

      // Preprocess data for yoy calculation
      const dataWithYOY = data.map((d, i) => {
        if (i >= 12) {
          const yoy = ((d.value / data[i - 12].value) - 1) * 100;
          return {...d, yoy};
        } else {
          return {...d, yoy: null}; // null if less than 12 months of data
        }
      });

      const dataSeries = dataWithYOY.map(d => d.value);
      const yoySeries = dataWithYOY.map(d => d.yoy).filter(d => d !== null);

      // Determine the height of the chart container
      const chartHeight = this.$refs.chart.$el.parentElement.clientHeight;
      console.warn(chartHeight)

      this.chartOptions = {
        title: {
          text: ''
        },
        chart: {
          backgroundColor: 'transparent',
          // height: chartHeight,
          zoomType: 'x',
          resetZoomButton: {
            theme: {
              fill: '#082f49',
              style: {
                color: 'white',
                fontWeight: 'bold'
              },
              r: 5,
              states: {
                hover: {
                  fill: '#d9534f',
                  style: {
                    color: 'white'
                  }
                }
              }
            },
            position: {
              align: 'left', 
              verticalAlign: 'top', 
              x: 10,
              y: 10
            }
          }
        },
        xAxis: [{
          type: 'datetime',
          crosshair: true,
          labels: {
            style: {
              color: '#ffffff'
            }
          },
          lineColor: '#808080',
          tickColor: '#808080'
        }],
        yAxis: [{
          labels: {
            format: '{value}',
            style: {
              color: '#ffffff'
            }
          },
          title: {
            text: 'Index',
            style: {
              color: '#ffffff'
            }
          },
          gridLineColor: '#808080' // Added this
        }, {
          title: {
            text: 'YoY%',
            style: {
              color: '#ffffff'
            }
          },
          labels: {
            format: '{value} %',
            style: {
              color: '#ffffff'
            }
          },
          gridLineColor: '#808080', // Added this
          opposite: true
        }],
        legend: {
          itemStyle: {
            color: '#ffffff' // Added this
          }
        },
        series: [{
          name: 'Index',
          data: dataWithYOY.map(d => [d.date, d.value])
        }, {
          name: 'YoY%',
          data: dataWithYOY.filter(d => d.yoy !== null).map(d => [d.date, d.yoy]),
          yAxis: 1
        }],
        tooltip: {
          shared: true
        },
        credits: {
          enabled: false
        },
        plotOptions: {
          series: {
            point: {
              events: {
                click: function(e) {
                  alert('You clicked on ' + e.point.category + ', value: ' + e.point.y);
                }
              }
            }
          }
        },
      };


    }

  },
  watch: {
    node() {
      this.fetchData();
    },
    country() {
      this.fetchData();
    },
  },
  created() {
    this.fetchData();
  },
}
</script>
