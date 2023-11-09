<template>
  <DxPieChart
    id="pie-chart"
    :data-source="getItemData()"
    :inner-radius="0.70"
    type="doughnut"
    center-template="centerTemplate"
    :startAngle="90 + 180 * (itemWeight / 1000)"
    containerBackgroundColor="transparent"
    :palette="['#0284c7', '#293a5e']"
  >
    <DxSeries
      argument-field="item"
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
    selectedNodeLabel: {
      type: String,
      required: true,
    },
    itemWeight: {
      type: Number,
      required: true,
    },
  },
  methods: {
    getItemData() {
      return [
        { item: this.selectedNodeLabel, weight: this.itemWeight, code: "item" },
        { item: "Rest of Items", weight: 1000 - this.itemWeight, code: "item" }
      ];
    },
    customizeLabel({ argumentText, valueText }) {
      return `${argumentText}\n${valueText}`;
    },
  },
};
</script>
