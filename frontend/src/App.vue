<template>
  <div id="app" class="bg-slate-950 h-screen flex p-4">
    <div class="w-3/4 flex flex-col overflow:auto">
      <div class="bg-slate-900 rounded-xl shadow-lg p-4 mb-4 h-50vh flex-grow">
        <div class="text-2xl font-bold mb-4">{{ selectedCountryLabel }} - {{ selectedNodeLabel }}</div>
        <SingleTimeSeries :node="selectedNode" :country="selectedCountry" />
      </div>
      <div class="bg-slate-900 rounded-xl shadow-lg pt-4 pr-4 pl-4 flex-grow h-30vh">
        <div class="text-2xl font-bold">Node weights</div>
        <div class="pies-container">
          <CountryItemWeight 
            :selectedNodeLabel="selectedNodeLabel"
            :itemWeight="itemWeight" 
          />
          <CountryWeight 
            :selectedCountry="selectedCountry"
            :countryWeight="countryWeight" 
            :selectedCountryLabel="selectedCountryLabel"
          />
          <FractionDisplay :fraction="countryWeight * itemWeight / 1000" :digits="3"/>
        </div>
      </div>
    </div>
    <div class="w-1/4 ml-4">
      <div class="bg-slate-900 rounded-xl shadow-lg p-4 h-full">
        <div class="text-2xl font-bold mb-4">Country</div>
        <div class="w-full mb-8">
          <div class="relative">
            <select v-model="selectedCountry" class="block appearance-none w-full bg-sky-900 text-white hover:border-sky-600 px-4 py-3 pr-8 shadow leading-tight focus:outline-none focus:shadow-outline rounded-xl">
              <option v-for="country in countries" :key="country.value" :value="country.value">
                {{ country.label }}
              </option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-slate-950">
              <svg class="fill-current h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M5.454 6.321l4.545 4.678 4.545-4.678-.707-.679-3.838 3.939-3.838-3.939-.707.679z"/></svg>
            </div>
          </div>
        </div>
        <div class="text-2xl font-bold mb-4">COICOP hierarchy</div>
        <div class="mb-2">
          <HierarchicalTable :items="items" @item-clicked="changeCode"/>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import HierarchicalTable from '@/components/HierarchicalTable.vue'
import SingleTimeSeries from '@/components/SingleTimeSeries.vue'
import CountryItemWeight from '@/components/CountryItemWeight.vue'
import CountryWeight from '@/components/CountryWeight.vue'
import FractionDisplay from '@/components/FractionDisplay.vue';

export default {
  name: 'App',
  components: {
    HierarchicalTable,
    SingleTimeSeries,
    CountryWeight,
    CountryItemWeight,
    FractionDisplay,
  },
  data() {
    return {
      items: [],
      countries: [],
      selectedCountry: "EA19",
      selectedNode: "00",
      selectedNodeLabel: "Harmonized overall",
      countryWeight: 1000,
      itemWeight: 1000,
    };
  },
  watch: {
    selectedCountry() {
      this.updateLayout();
    }
  },
  async created() {
    try {
      const response = await axios.get('/node/00')
      this.items = response.data
    } catch (error) {
      console.error(error)
    }
    try {
      const response = await axios.get('/countries')
      this.countries = response.data
    } catch (error) {
      console.error(error);
    }
    this.updateLayout()
  },
  methods: {
    changeCode (code, label) {
      this.selectedNode = code;
      this.selectedNodeLabel = label
      this.updateLayout()
    },
    updateLayout() {
      console.log("Current selection: " + this.selectedCountry + " " + this.selectedNode)
      this.updateWeights()
    },
    async updateWeights() {
      const response = await axios.get(`/weights/${this.selectedCountry}/${this.selectedNode}`)
      this.itemWeight = response.data.item
      this.countryWeight = response.data.country
    },
  },
  computed: {
    selectedCountryLabel() {
      const country = this.countries.find(country => country.value === this.selectedCountry)
      return country ? country.label : ''
    }
  }
}
</script>

<style>
body {
  margin: 0px !important;
  overflow-y: hidden;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #bdc6d0;
}

.pies-container {
  display: flex;
  align-items: center;
  max-height: 30vh;
}

.pies-container > div {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
}
</style>
