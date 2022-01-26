<template>
  <div id="mind-map">
    <div id="map" />
  </div>
</template>

<script>
import MindElixir, { E } from 'mind-elixir'
import { getLabelArch } from '@/api/label-arch'
import { buildLabelArch, buildStockLabels } from '@/utils/build-label-arch'

export default {
  name: 'StockData',
  data() {
    return {
      ME: null,
      labelArch: null,
      stockLabels: null
    }
  },
  computed: {
    lables() {
      return this.$store.getters.stock_labels
    }
  },
  watch: {
    lables(val) {
      this.appendStockLabels(val)
    }
  },
  created() {
    // 获取参数
    if (typeof this.$route.query.code === 'undefined') {
        // 调试提示
        console.log('未传入股票代码')
        this.stockLabels = this.$store.getters.stock_labels
    } else {
        this.$store.dispatch('stock/fetchStockLabels', this.$route.query)
    }
  },
  mounted() {
    this.fetchLabelArch('stock_frame').then(() => {
      this.ME = new MindElixir({
        el: '#map',
        direction: MindElixir.SIDE,
        data: {
          nodeData: buildLabelArch(this.labelArch),
          linkData: {}
        },
        draggable: true, // default true
        contextMenu: true, // default true
        toolBar: true, // default true
        nodeMenu: true, // default true
        keypress: true, // default true
        primaryNodeVerticalGap: 15,
        primaryNodeHorizontalGap: 15
        // overflowHidden: true // default false
      })
      this.ME.init()
      this.appendStockLabels(this.stockLabels)
    })
  },
  methods: {
    async fetchLabelArch(archName) {
      await getLabelArch(archName).then(response => {
        this.labelArch = response.data
      })
    },
    appendStockLabels(labels) {
      if (this.labelArch != null && labels != null) {
        this.ME = new MindElixir({
          el: '#map',
          direction: MindElixir.SIDE,
          data: {
            nodeData: buildStockLabels(this.labelArch, labels),
            linkData: {}
          },
          draggable: true, // default true
          contextMenu: true, // default true
          toolBar: true, // default true
          nodeMenu: true, // default true
          keypress: true, // default true
          primaryNodeVerticalGap: 15,
          primaryNodeHorizontalGap: 15
          // overflowHidden: true // default false
        })
        this.ME.init()
      }
    }
  }
}
</script>

<style>
  #map {
    height: 668px;
    width: 100%;
    overflow: auto;
  }
</style>
