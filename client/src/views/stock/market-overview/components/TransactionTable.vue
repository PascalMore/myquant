<template>
  <div style='padding: 0px;' >
    <div style='padding-bottom: 2px;' class="filter-container">
      <el-date-picker v-model="listQuery.notice_date" type="date" placeholder="公告日期" value-format="yyyyMMdd" class="filter-item" style="width: 150px" />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        {{ $t('table.search') }}
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        {{ $t('table.export') }}
      </el-button>
    </div>
    <el-table :data="pagedList" :row-style="{height: '15px'}"  v-loading="listLoading" style="width: 100%;padding-top: 8px;">
        <el-table-column label="公告日期" width="90" align="center">
        <template slot-scope="{row}">
            {{ row.notice_date}}
        </template>
        </el-table-column>
        <el-table-column label="股票代码" width="100">
        <template slot-scope="{row}">
            {{ row.stock_id}}
        </template>
        </el-table-column>
        <el-table-column label="股票名称" width="80" align="center">
        <template slot-scope="{row}">
            {{ row.stock_name }}
        </template>
        </el-table-column>
        <el-table-column show-overflow-tooltip label="业绩指标" width="150" align="center">
        <template slot-scope="{row}">
            {{ row.predict_finance }}
        </template>
        </el-table-column>
        <el-table-column label="变动方向" width="80" align="center">
        <template slot-scope="{row}">
            {{ row.predict_type }}
        </template>
        </el-table-column>
        <el-table-column show-overflow-tooltip label="业绩变动" width="285" align="center">
        <template slot-scope="{row}">
            {{ row.predict_content }}
        </template>
        </el-table-column>
        <!-- <el-table-column label="预告数值" width="100" align="center">
        <template slot-scope="scope">
            ¥{{ scope.row.price | toThousandFilter }}
        </template>
        </el-table-column> -->
        <el-table-column label="去年同期" width="100" align="center">
        <template slot-scope="{row}">
            {{ row.preyear_same_period }}
        </template>
        </el-table-column>
        <el-table-column label="变动幅度" width="150" align="center">
        <template slot-scope="{row}">
            {{ row.predict_val_chg }}
        </template>
        </el-table-column>
        <el-table-column show-overflow-tooltip label="业绩解释" width="285" align="center">
        <template slot-scope="{row}">
            {{ row.change_explain }}
        </template>
        </el-table-column>
        <el-table-column label="报告期" width="100" align="center">
        <template slot-scope="{row}">
            {{ row.rpt_date }}
        </template>
        </el-table-column>
    </el-table>
    <pagination style="margin-top:12px; padding-top: 8px;padding-bottom: 2px" v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="pageShow" />
  </div>
</template>

<script>
import { fetchStockNoticeAdv } from '@/api/stock-notice-adv'
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

export default {
  name: 'StockNotice',
  components: { Pagination },  
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
      pagedList: null,
      total: 0,
      listLoading: false,
      listQuery: {
        page: 1,
        limit: 10,
        sort: '',
        notice_date: undefined
      },
      downloadLoading: false,
      code_name: null
    }
  },
  created() {
    this.fetchData()
    this.code_name = this.generateCodeNames(JSON.parse(localStorage.getItem('stock_list')))
  },
  methods: {
    pageShow() {
      // 如果list为空的时候，获取数据
      if(!this.list && typeof(this.list)!="undefined" && this.list != 0) {
        this.getList()
      } else {
        this.pagedList = this.list.slice((this.listQuery.page - 1) * this.listQuery.limit, this.listQuery.page * this.listQuery.limit)
      }
    },
    handleFilter() {
      this.listQuery.page = 1
      this.fetchData()
    },
    handleDownload() {
      console.log('TODO handleDownload')
    },
    fetchData() {
      fetchStockNoticeAdv(this.listQuery).then(response => {
        var res = []
        var cnt = 1
        console.log(response.data)
        if (Object.prototype.toString.call(response.data) === '[object Array]') {
          response.data.forEach((d, i, arr1) => {
            var tmp = {}
            tmp['notice_date'] = d['notice_date']
            tmp['stock_id'] = d['stock_id']
            tmp['stock_name'] = this.code_name[d['stock_id'].substring(0, 6)]
            tmp['predict_finance'] = d['predict_finance']
            tmp['predict_type'] = d['predict_type']
            tmp['predict_content'] = d['predict_content']
            tmp['preyear_same_period'] = d['preyear_same_period']
            tmp['predict_val_chg'] = d['add_amp_lower'] + "% - " +  d['add_amp_upper'] + "%"
            tmp['change_explain'] = d['change_explain']
            tmp['rpt_date'] = d['rpt_date']
            res.push(tmp)
          })
        } else {
          console.log("没有获得任何业绩预告")
        }

        this.list = res
        this.total = this.list.length
        // 分页展示
        this.pageShow()
        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
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
