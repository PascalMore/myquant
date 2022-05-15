<template>
  <el-table v-loading="loading"  element-loading-text="请给我点时间！" :data="list" border fit highlight-current-row style="width: 100%">
    <el-table-column :label="$t('table.id')" prop="id" sortable="custom" align="center" width="80" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
    </el-table-column>
    <el-table-column width="80" label="股票代码" align="center">
      <template slot-scope="{row}">
        <router-link :to="{ path:'/stock/stock-data', query: {code: row.asset_id}}">{{ row.asset_id }}</router-link>
      </template>
    </el-table-column>
    <el-table-column width="180px" align="center" label="股票名称">
      <template slot-scope="{row}">
        <span>{{ row.asset_name }}</span>
      </template>
    </el-table-column>
    <el-table-column width="180px" align="center" label="入池日期">
      <template slot-scope="{row}">
        <span>{{ row.import_date }}</span>
      </template>
    </el-table-column>

    <el-table-column min-width="300px" label="入池类型">
      <template slot-scope="{row}">
        <span>{{ row.pool_type }}</span>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import { fetchStockPool } from '@/api/stock-pool'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  props: {
    type: {
      type: String,
      default: 'basic'
    }
  },
  data() {
    return {
      list: null,
      listQuery: {
        page: 1,
        limit: 5,
        pool_type: this.type,
        pool_date: undefined,
        sort: '+id'
      },
      loading: true,
      code_name: null
    }
  },
  created() {
    this.getList()
    this.code_name = this.generateCodeNames(JSON.parse(localStorage.getItem('stock_list')))
  },
  methods: {
    getList() {
      this.loading = true
      //this.$emit('create') // for test
      fetchStockPool(this.listQuery).then(response => {
        var res = []
        var cnt = 1
        response.data.forEach((d, i, arr1) => {
            var tmp = d
            tmp['id'] = cnt++
            tmp['asset_id'] = d['asset_id']
            tmp['import_date'] = d['import_date']
            tmp['pool_type'] = d['pool_type']
            tmp['asset_name'] = this.code_name[d['asset_id']]
            res.push(tmp)
          })
        this.list = res
        this.loading = false
      })
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
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

