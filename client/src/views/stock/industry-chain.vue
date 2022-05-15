<template>
  <div id="mind-map">
    <div id="industry-list">
      <span>产业链分析：</span>
      <el-select style="width:180px" v-model="options.value" placeholder="请选择" @change="selectChanged">
        <el-option-group
          v-for="group in options"
          :key="group.label"
          :label="group.label">
          <el-option
            v-for="item in group.options"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-option-group>
      </el-select>
    </div>
    <div id="map" />
  </div>
</template>

<script>
import MindElixir, { E } from 'mind-elixir'
import { getLabelArch, getAllIndustryChain } from '@/api/label-arch'
import { buildLabelArch, buildStockLabels } from '@/utils/build-label-arch'

export default {
  name: 'IndustryChain',
  data() {
    return {
      ME: null,
      labelArch: null,
      stockLabels: null,
      label_arch_type: "产业链研究",
      options: [],
      mapping: {
        "industry_electric": "电气设备",
        "industry_tmt": "TMT",
        "industry_metal": "有色金属"
      }
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
   
    getAllIndustryChain(this.label_arch_type).then(response => {
      var tmp_dd = {}
      response.data.forEach((d, i, arr1) => {
        var grp_name = this.mapping[this.getIndustry(d['label_arch_id'])]
        if (Object.prototype.hasOwnProperty.call(tmp_dd, grp_name)) {
          tmp_dd[grp_name].push({ value: d['label_arch_id'], label: d['label_name'] })
        } else {
          tmp_dd[grp_name] = [{ value:  d['label_arch_id'], label: d['label_name'] }]
        }
      })
      for (var k in tmp_dd) {
        this.options.push({"label": k, "options": tmp_dd[k]})
      }
      //console.log(this.options)
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
    },
    getIndustry(name){
      var r = name.split("_")
      return r[0] + "_" + r[1]
    },
    selectChanged(value) {
      this.fetchLabelArch(value).then(() => {
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
        primaryLinkStyle: 2,
        primaryNodeVerticalGap: 15,
        primaryNodeHorizontalGap: 15
        // overflowHidden: true // default false
      })
      this.ME.init()
      this.appendStockLabels(this.stockLabels)
    })
    }
  }
}
</script>

<style>
  #mind-map {
    position: relative;
    margin: 2px;
  }
  #map {
    height: 600px;
    width: 100%;
    overflow: auto;
  }
  #industry-list {
    height: 37px;
    width: 100%;
  }
</style>
