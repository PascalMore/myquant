<template>
  <div class="app-container" style='padding: 12px;' >
    <div style='padding-bottom: 2px;' class="filter-container">
      <el-select v-model="listQuery.strategy_id" placeholder="策略ID" clearable style="width: 150px" class="filter-item">
        <el-option v-for="item in strategyList" :key="item" :label="item" :value="item" />
      </el-select>
      <el-date-picker v-model="listQuery.exe_date" type="date" placeholder="执行日期" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px" />
      <el-select v-model="listQuery.sort" placeholder="排序方式" style="width: 150px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        {{ $t('table.search') }}
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        {{ $t('table.export') }}
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="pagedList"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
    >
      <el-table-column :label="$t('table.id')" prop="id" sortable="custom" align="center" width="80" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.date')" width="100px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.exe_date | parseTime('{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="策略名称" min-width="120px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.strategy_id }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.author')" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.author }}</span>
        </template>
      </el-table-column>
      <el-table-column label="股票代码" width="80px">
        <template slot-scope="{row}">
          <router-link :to="{ path:'/stock/stock-data', query: {code: row.asset_id}}">{{ row.asset_id }}</router-link>
        </template>
      </el-table-column>
      <el-table-column label="股票名称" align="center" width="95">
        <template slot-scope="{row}">
          <span>{{ row.asset_name }}</span>
        </template>
      </el-table-column>
    </el-table>

    <pagination style="margin-top:12px; padding-top: 8px;padding-bottom: 2px" v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="pageShow" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="70px" style="width: 400px; margin-left:50px;">
        <el-form-item :label="$t('table.date')" prop="timestamp">
          <el-date-picker v-model="temp.timestamp" type="datetime" placeholder="Please pick a date" />
        </el-form-item>
        <el-form-item :label="$t('table.title')" prop="title">
          <el-input v-model="temp.title" />
        </el-form-item>
        <el-form-item :label="$t('table.importance')">
          <el-rate v-model="temp.importance" :colors="['#99A9BF', '#F7BA2A', '#FF9900']" :max="3" style="margin-top:8px;" />
        </el-form-item>
        <el-form-item :label="$t('table.remark')">
          <el-input v-model="temp.remark" :autosize="{ minRows: 2, maxRows: 4}" type="textarea" placeholder="Please input" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          {{ $t('table.cancel') }}
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          {{ $t('table.confirm') }}
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :visible.sync="dialogPvVisible" title="Reading statistics">
      <el-table :data="pvData" border fit highlight-current-row style="width: 100%">
        <el-table-column prop="key" label="Channel" />
        <el-table-column prop="pv" label="Pv" />
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogPvVisible = false">{{ $t('table.confirm') }}</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { fetchStrategyExecutions } from '@/api/strategy'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

export default {
  name: 'QuantSelection',
  components: { Pagination },
  directives: { waves },
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
  data() {
    return {
      tableKey: 0,
      list: null,
      pagedList: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 10,
        strategy_id: undefined,
        exe_date: undefined,
        sort: ''
      },
      strategyList: ['BottomLaunch', 'TrendBack', 'ShockBottom'],
      sortOptions: [{ label: 'Date Ascending', key: '+date' }, { label: 'Date Descending', key: '-date' }],
      code_name: null,
      temp: {
        id: undefined,
        strategy: '',
        exe_date: new Date(),
        author: '',
        stock_code: '',
        stock_name: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
        type: [{ required: true, message: 'type is required', trigger: 'change' }],
        timestamp: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'change' }],
        title: [{ required: true, message: 'title is required', trigger: 'blur' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.code_name = this.generateCodeNames(JSON.parse(localStorage.getItem('stock_list')))
    this.getList()
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
    getList() {
      this.listLoading = true
      fetchStrategyExecutions(this.listQuery).then(response => {
        var res = []
        var cnt = 1
        if (Object.prototype.toString.call(response.data) === '[object Array]') {
          response.data.forEach((d, i, arr1) => {
            d['strategy_res'].forEach((dd, ii, arr2) => {
              var tmp = dd
              tmp['id'] = cnt++
              tmp['author'] = d['user']
              tmp['exe_date'] = d['exe_date']
              tmp['strategy_id'] = d['strategy_id']
              tmp['asset_name'] = this.code_name[dd['asset_id']]
              res.push(tmp)
            })
          })
        } else {
          response.data['strategy_res'].forEach((dd, ii, arr2) => {
            var tmp = dd
            tmp['id'] = cnt++
            tmp['author'] = response.data['user']
            tmp['exe_date'] = response.data['exe_date']
            tmp['strategy_id'] = response.data['strategy_id']
            tmp['asset_name'] = this.code_name[dd['asset_id']]
            res.push(tmp)
          })
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
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: '操作成功',
        type: 'success'
      })
      row.status = status
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        importance: 1,
        remark: '',
        timestamp: new Date(),
        title: '',
        status: 'published',
        type: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          this.temp.id = parseInt(Math.random() * 100) + 1024 // mock a id
          this.temp.author = 'vue-element-admin'
          createArticle(this.temp).then(() => {
            this.list.unshift(this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: '成功',
              message: '创建成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.timestamp = new Date(this.temp.timestamp)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.timestamp = +new Date(tempData.timestamp) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
          updateArticle(tempData).then(() => {
            const index = this.list.findIndex(v => v.id === this.temp.id)
            this.list.splice(index, 1, this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: '成功',
              message: '更新成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleDelete(row, index) {
      this.$notify({
        title: '成功',
        message: '删除成功',
        type: 'success',
        duration: 2000
      })
      this.list.splice(index, 1)
    },
    handleFetchPv(pv) {
      fetchPv(pv).then(response => {
        this.pvData = response.data.pvData
        this.dialogPvVisible = true
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['timestamp', 'title', 'type', 'importance', 'status']
        const filterVal = ['timestamp', 'title', 'type', 'importance', 'status']
        const data = this.formatJson(filterVal)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'table-list'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal) {
      return this.list.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    }
  }
}
</script>
