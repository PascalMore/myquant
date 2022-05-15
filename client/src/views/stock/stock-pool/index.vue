<template>
  <div class="tab-container">
    <el-tag>mounted times ：{{ createdTimes }}</el-tag>
    <el-alert :closable="false" style="width:200px;display:inline-block;vertical-align: middle;margin-left:30px;" title="Tab with keep-alive" type="success" />
    <el-date-picker v-model="listQuery.pool_date" type="date" placeholder="入池日期" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px" />
    <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        {{ $t('table.search') }}
    </el-button>
    <el-tabs v-model="activeName" style="margin-top:15px;" type="border-card">
      <el-tab-pane v-for="item in tabMapOptions" :key="item.key" :label="item.label" :name="item.key">
        <keep-alive>
          <tab-pane v-if="activeName==item.key" :type="item.key" @create="showCreatedTimes" />
        </keep-alive>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import TabPane from './components/TabPane'

export default {
  name: 'Tab',
  directives: { waves },
  components: { TabPane },
  data() {
    return {
      tabMapOptions: [
        { label: '基础池', key: 'basic' },
        { label: '重点池', key: 'important' },
        { label: '策略-深度价值', key: 'deep' }
      ],
      listQuery : {
        pool_date: undefined,
      },
      activeName: 'basic',
      createdTimes: 0
    }
  },
  watch: {
    activeName(val) {
      this.$router.push(`${this.$route.path}?tab=${val}`)
    }
  },
  created() {
    // init the default selected tab
    const tab = this.$route.query.tab
    if (tab) {
      this.activeName = tab
    }
  },
  methods: {
    showCreatedTimes() {
      this.createdTimes = this.createdTimes + 1
    },
    handleFilter() {
    },
  }
}
</script>

<style scoped>
  .tab-container {
    margin: 30px;
  }
</style>
