<template>
  <div style='padding: 0px;' >
    <!-- <div style='padding-bottom: 2px;' class="filter-container">
      <el-date-picker v-model="listQuery.notice_date" type="date" placeholder="公告日期" value-format="yyyyMMdd" class="filter-item" style="width: 150px" />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        {{ $t('table.search') }}
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        {{ $t('table.export') }}
      </el-button>
    </div> -->
    <div>全市场收益率概览</div>
    <el-table :data="list" :row-style="{height: '14px'}"  v-loading="listLoading" style="width: 100%;padding-top: 8px;font-size:14px">
        <el-table-column label="最新日期" width="93" align="center">
        <template slot-scope="{row}">
            {{ row.calc_date}}
        </template>
        </el-table-column>
        <el-table-column label="指数代码" width="77">
        <template slot-scope="{row}">
            {{ row.index_id}}
        </template>
        </el-table-column>
        <el-table-column label="指数名称" width="80" align="center">
        <template slot-scope="{row}">
            {{ row.index_name }}
        </template>
        </el-table-column>
        <el-table-column show-overflow-tooltip label="当日" width="70" align="center" >
        <template slot-scope="{row}">
            {{ (row.cur_td*100).toFixed(2) + "%" }}
        </template>
        </el-table-column>
        <el-table-column show-overflow-tooltip label="本周" width="70" align="center">
        <template slot-scope="{row}">
            {{ (row.cur_week*100).toFixed(2) + "%" }}
        </template>
        </el-table-column>
        <el-table-column show-overflow-tooltip label="本月" width="70" align="center">
        <template slot-scope="{row}">
            {{ (row.cur_mon*100).toFixed(2) + "%" }}
        </template>
        </el-table-column>
        <el-table-column show-overflow-tooltip label="本季" width="70" align="center">
        <template slot-scope="{row}">
            {{ (row.cur_quart*100).toFixed(2) + "%" }}
        </template>
        </el-table-column>
        <el-table-column show-overflow-tooltip label="YTD" width="70" align="center">
        <template slot-scope="{row}">
            {{ (row.cur_ytd*100).toFixed(2) + "%" }}
        </template>
        </el-table-column>
        <el-table-column show-overflow-tooltip v-for="item in table_head_m" :label="item.label" :key="item.prop" width="70" align="center">
          <template slot-scope="{row}">
            {{  (row[item.prop]*100).toFixed(2) + "%"}}
          </template>
        </el-table-column>
        <el-table-column show-overflow-tooltip v-for="item in table_head_y" :label="item.label" :key="item.prop" width="70" align="center">
          <template slot-scope="{row}">
            {{  row[item.prop] === null ? "-" : (row[item.prop]*100).toFixed(2) + "%"}}
          </template>
        </el-table-column>
        <el-table-column show-overflow-tooltip label="近1周" width="70" align="center">
        <template slot-scope="{row}">
            {{ (row.last_1w*100).toFixed(2) + "%" }}
        </template>
        </el-table-column>
        <el-table-column show-overflow-tooltip label="近2周" width="70" align="center">
        <template slot-scope="{row}">
            {{ (row.last_2w*100).toFixed(2) + "%" }}
        </template>
        </el-table-column>
        <el-table-column show-overflow-tooltip label="近1月" width="70" align="center">
        <template slot-scope="{row}">
            {{ (row.last_1m*100).toFixed(2) + "%" }}
        </template>
        </el-table-column>
        <el-table-column show-overflow-tooltip label="近3月" width="70" align="center">
        <template slot-scope="{row}">
            {{ (row.last_3m*100).toFixed(2) + "%" }}
        </template>
        </el-table-column>
        <el-table-column show-overflow-tooltip label="近6月" width="70" align="center">
        <template slot-scope="{row}">
            {{ (row.last_6m*100).toFixed(2) + "%" }}
        </template>
        </el-table-column>
        <el-table-column show-overflow-tooltip label="近1年" width="70" align="center">
        <template slot-scope="{row}">
            {{ (row.last_1y*100).toFixed(2) + "%" }}
        </template>
        </el-table-column>
    </el-table>
    <!-- <pagination style="margin-top:12px; padding-top: 8px;padding-bottom: 2px" v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="pageShow" /> -->
  </div>
</template>

<script>
import { fetchIndexYields } from '@/api/index'
import waves from '@/directive/waves' // waves directive

export default {
  name: 'AssetYield',
  components: {  },  
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        success: 'success',
        pending: 'danger'
      }
      return statusMap[status]
    },
    orderNoFilter(str) {
      return str.substring(0, 30)
    }
  },
  data() {
    return {
      list: null,
    //   pagedList: null,
    //   total: 0,
      listLoading: false,
      listQuery: {
        page: 1,
        limit: 10,
        sort: '',
        index_list: '',
        calc_date: '',
        interval_list: ''
      },
      downloadLoading: false,
      code_name: null,
      table_head_m: [],
      table_head_y: [],
      index_ids: ['000300','000852', '399006', '000688','159920','513130','513500','513000','164824','513080','513030','511260','511030'],
      index_name: {
        '000300': '沪深300',
        '000852': '中证1000',
        '399006': '创业板',
        '000688': '科创50',
        '159920': '恒生指数',
        '513130': '恒生科技',
        '513500': '标普500',
        '513300': '纳斯达克',
        '513000': '日经225',
        '164824': '印度',
        '513080': '法国',
        '513030': '德国',
        '511260': '利率债',
        '511030': '信用债'
      }
    }
  },
  created() {
    this.genIntervalList()
    this.initTableHead()
    this.fetchData()
    this.code_name = this.generateCodeNames(JSON.parse(localStorage.getItem('stock_list')))
  },
  methods: {
    handleDownload() {
      console.log('TODO handleDownload')
    },
    initTableHead() {
      this.table_head_m = this.listQuery['interval_list'].split(',').map((item, index) =>{
        if (item.startsWith('m')) {
          return {'label': item.split('_').slice(-1) + '月', 'prop': item}
        }
      }).filter(l => l != undefined)
      this.table_head_y = this.listQuery['interval_list'].split(',').map((item, index) =>{
        if (item.startsWith('y')) {
          return {'label': item.split('_').slice(-1) + '年', 'prop': item}
        }
      }).filter(l => l != undefined)
    //   console.log(this.table_head_m)
    },
    genIntervalList() {
      var res = []
      //1.本周期
      res = res.concat(['cur_td','cur_week','cur_mon','cur_quart','cur_ytd'])
      //2.月份 m_1,m_2
      var dt = new Date()
      let mon = dt.getMonth()
      for(var i=1; i<mon+1; i++) {
        res.push("m_" + i)
      }
      //3.年份 y_ 2021,y_2022
      let year =dt.getFullYear()
      res.push("y_" + (year - 1))
      res.push("y_" + (year - 2))
      //4. last
      res = res.concat(['last_1w','last_2w','last_1m', 'last_2m', 'last_3m', 'last_6m', 'last_1y'])

      this.listQuery['interval_list'] = res.join(',')
    },
    fetchData() {
      this.listLoading = true
      // 设置查询参数
      var dt = new Date()
      let year = dt.getFullYear()
      let mon = (dt.getMonth() + 1).toString().padStart(2, '0')
      let day = dt.getDate().toString().padStart(2, '0')
      this.listQuery['calc_date'] = year + '-' + mon +  '-' + day
      this.listQuery['index_list'] = this.index_ids.join(',')
      fetchIndexYields(this.listQuery).then(response => {
        var res = []
        var cnt = 1
        console.log(response.data)
        if (Object.prototype.toString.call(response.data) === '[object Array]') {
          response.data.forEach((d, i, arr1) => {
            var tmp = {}
            tmp['calc_date'] = d['calc_date']
            tmp['index_id'] = d['index_id']
            tmp['index_name'] = this.index_name[d['index_id']]
            this.listQuery['interval_list'].split(',').forEach((y, ii , l) => {
              tmp[y] = d['index_yields'][y]
            })
            res.push(tmp)
          })
          console.log(res)
        } else {
          console.log("没有获得任何市场收益率数据")
        }
        this.list = res
        this.listLoading = false
      })
    },
    generateCodeNames(codes) {
      const res = {}
      for (const stk of codes) {
        res[stk.code] = stk.name
      }
      return res
    }
  }
}
</script>
