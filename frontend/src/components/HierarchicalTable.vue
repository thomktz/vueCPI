<template>
  <div class="tree-view">
    <table class="table">
      <tr v-for="(item, index) in items" :key="index" class="tree-row">
        <td>
          <div :style="{ 'padding-left': `${(item.depth-1) * 10}px` }">
            <div :class="`label-pill depth-${item.depth}`">
              <div class="pill-content">
                <button v-if="item.children && item.children.length" class="expand-button" @click="toggleChildren(item)">
                  <span v-if="item.isExpanded">↑</span>
                  <span v-else>↓</span>
                </button>
                <div class="label" :title="item.label">
                  {{ item.label }}
                </div>
                <div class="code">{{ item.code }}</div>
                <span class="play-button" @click="onPlay(item.code, item.label)">&#9658;</span>
              </div>
            </div>
          </div>
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      items: [],
    };
  },
  async created() {
    await this.toggleChildren({ label: 'Root', children: ['00'], depth: 0 })
    this.toggleChildren(this.items[0])
  },
  methods: {
    async toggleChildren(item) {
      console.log('Toggle children for item: ', item);
      try {
        const parentIndex = this.items.indexOf(item);

        if (item.isExpanded) {
          // Item is already expanded, collapse it
          item.isExpanded = false;
          this.removeChildren(item.label);
        } else {
          // Item is collapsed, expand it
          item.isExpanded = true;

          for (const childCode of [...item.children].reverse()) { // Reverse the order and copy
            const response = await axios.get(`/node/${childCode}`);
            response.data.depth = item.depth + 1;
            response.data.parent = item.label;
            response.data.code = childCode; // Adding the code here
            this.items.splice(parentIndex + 1, 0, response.data);
          }
        }
      } catch (error) {
        console.error(error);
      }
    },
    removeChildren(parentLabel) {
      // Filter out the direct children
      let directChildren = this.items.filter(item => item.parent === parentLabel);
      this.items = this.items.filter(item => item.parent !== parentLabel);

      // Recursively remove any nested children
      directChildren.forEach(child => {
        this.removeChildren(child.label);
      });
    },
    onPlay(code, label) {
      this.$emit('item-clicked', code, label);
    },
  },

};
</script>

<style scoped>
.table {
  width: 100%;
  max-width: 100%;
  overflow-x: auto;
  min-width: 0;

}

.label {
  overflow: hidden;
  text-overflow: ellipsis;
  padding-left: 5px;
}

.pill-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 0 5px;
}

.label-pill {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 8px 10px;
  border-radius: 10px;
  margin: 0;
  color: white;
  box-sizing: border-box;
  overflow: hidden;
}

.expand-button {
  background: none;
  border: none;
  color: #001046;
  padding-right: 5px;
  font-size: 16px;
  cursor: pointer;
}

.expand-button:hover {
  color: #ffffff;
}

.play-button {
  color: #001046;
  font-size: 14px;
  cursor: pointer;
  margin-left: 7px;
}

.play-button:hover {
  color: #ffffff;
}

.code {
  font-size: 12px;
  text-align: right;
  flex-grow: 1;
  color: black;
}

.depth-0 {
  background-color: rgb(8 47 73);
  color: white;
}

.depth-1 {
  background-color: rgb(12 74 110);
  color: white;
}

.depth-2 {
  background-color: rgb(7 89 133);
  color: white;
}

.depth-3 {
  background-color: rgb(3 105 161);
  color: white;
}

.depth-4 {
  background-color: rgb(2 132 199);
  color: white;
}

.depth-5 {
  background-color: rgb(14 165 233);
  color: white;
}
</style>
