<template>
  <DxPieChart
    id="pie-chart-country"
    :data-source="getCountryData()"
    :inner-radius="0.70"
    type="doughnut"
    center-template="centerTemplate"
    :startAngle="90 + 180 * (countryWeight / 1000)"
    containerBackgroundColor="transparent"
    :palette="['#0284c7', '#293a5e']"
  >
    <DxSeries
      argument-field="country"
      value-field="weight"
    >
      <DxLabel
        :visible="true"
        :customize-text="customizeLabel"
        background-color="none"
        format="fixedPoint"
      >
        <DxConnector :visible="true"/>
      </DxLabel>
    </DxSeries>
    <DxLegend :visible="false"/>
    <template #centerTemplate="data">
      <CenterTemplate :pie-chart="data.data"/>
    </template>
  </DxPieChart>
</template>

<script>
import {
  DxPieChart, DxSeries, DxLabel, DxConnector, DxLegend
} from 'devextreme-vue/pie-chart';
import CenterTemplate from './CenterTemplate.vue';

export default {
  components: {
    DxPieChart, DxSeries, DxLabel, DxConnector, DxLegend, CenterTemplate,
  },
  props: {
    selectedCountryLabel: {
      type: String,
      required: true,
    },
    selectedCountry: {
      type: String,
      required: true,
    },
    countryWeight: {
      type: Number,
      required: true,
    },
  },
  methods: {
    getCountryData() {
      console.log("In getCountryData, ", this.selectedCountryLabel)
      return [
        { country: this.selectedCountryLabel, weight: this.countryWeight, code: this.selectedCountry },
        { country: "Rest of EA", weight: 1000 - this.countryWeight, code: this.selectedCountry }
      ];
    },
    customizeLabel({ argumentText, valueText }) {
      return `${argumentText}`;
    },
  },
};
</script>

