<template>
  <el-row :gutter="40" class="panel-group">
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('newVisitis')">
        <div class="card-panel-icon-wrapper icon-people">
          <svg-icon icon-class="peoples" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            {{mkt_status}}
          </div>
          <count-to :start-val="0" :end-val="mkt_temper" :duration="2600" :decimals=4 class="card-panel-num" />
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('messages')">
        <div class="card-panel-icon-wrapper icon-message">
          <svg-icon icon-class="message" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            Messages
          </div>
          <count-to :start-val="0" :end-val="81212" :duration="3000" class="card-panel-num" />
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('purchases')">
        <div class="card-panel-icon-wrapper icon-money">
          <svg-icon icon-class="money" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            Purchases
          </div>
          <count-to :start-val="0" :end-val="9280" :duration="3200" class="card-panel-num" />
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" @click="handleSetLineChartData('shoppings')">
        <div class="card-panel-icon-wrapper icon-shopping">
          <svg-icon icon-class="shopping" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            Shoppings
          </div>
          <count-to :start-val="0" :end-val="13600" :duration="3600" class="card-panel-num" />
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import CountTo from 'vue-count-to'
import { fetchIndicators } from '@/api/indicator'

export default {
  components: {
    CountTo
  },
  data() {
    return {
      mkt_temper: 0.0,
      mkt_status:""
    } 
  },
  created() {
    this.getMarketTemper()
  },
  methods: {
    dateFormat(time) {
      var date=new Date(time);
      var year=date.getFullYear();
      /* 在日期格式中，月份是从0开始的，因此要加0
       * 使用三元表达式在小于10的前面加0，以达到格式统一  如 09:11:05
      * */
      var month= date.getMonth()+1<10 ? "0"+(date.getMonth()+1) : date.getMonth()+1;
      var day=date.getDate()<10 ? "0"+date.getDate() : date.getDate();
      //var hours=date.getHours()<10 ? "0"+date.getHours() : date.getHours();
      //var minutes=date.getMinutes()<10 ? "0"+date.getMinutes() : date.getMinutes();
      //var seconds=date.getSeconds()<10 ? "0"+date.getSeconds() : date.getSeconds();
      // 拼接
      return year+"-"+month+"-"+day;
    },
    processMktStatus(val) {
      if (-0.2 < val && val < 0.2) {
        this.mkt_status = "清淡震荡"
      } else {
        var tmp = ""
        if (val > 0) {
          tmp = "上涨"
          if (0.2 <= val && val < 0.41) {
            this.mkt_status = "温和"
          } else if(0.41 <= val && val < 0.85) {
           this.mkt_status = "小幅"
          } else if(0.85 <= val && val < 1.57) {
            this.mkt_status = "大幅"
          } else if(1.57 <= val && val < 3.28) {
            this.mkt_status = "疯狂"
          } else {
            this.mkt_status = "爆炸"
          }
          this.mkt_status = this.mkt_status + tmp
        } else {
          tmp = "下跌"
          if (-0.2 >= val && val > -0.41) {
            this.mkt_status = "温和"
            } else if(-0.41 >= val && val > -0.85) {
              this.mkt_status = "小幅"
            } else if(-0.85 >= val && val > -1.57) {
              this.mkt_status = "大幅"
            } else if(-1.57 >= val && val >- 3.28) {
              this.mkt_status = "疯狂"
            } else {
              this.mkt_status = "爆炸"
            }
            this.mkt_status = this.mkt_status + tmp
        }
      }
    },
    handleSetLineChartData(type) {
      this.$emit('handleSetLineChartData', type)
    },
    getMarketTemper() {
      var td  = this.dateFormat(new Date())
      fetchIndicators({"ind":"mkt_temper_td", "date": td}).then(response => {
        if (Object.prototype.toString.call(response.data) === '[object Array]') {
          response.data.some((d) => {
            if (d['asset_id'] === '000000') {
              this.mkt_temper = d['value']
              this.processMktStatus(this.mkt_temper)
              console.log(this.mkt_status)
              return true
            }
          })
        } else {
            console.log("Debug, No indicator")
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.panel-group {
  margin-top: 18px;

  .card-panel-col {
    margin-bottom: 32px;
  }

  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-people {
        background: #40c9c6;
      }

      .icon-message {
        background: #36a3f7;
      }

      .icon-money {
        background: #f4516c;
      }

      .icon-shopping {
        background: #34bfa3
      }
    }

    .icon-people {
      color: #40c9c6;
    }

    .icon-message {
      color: #36a3f7;
    }

    .icon-money {
      color: #f4516c;
    }

    .icon-shopping {
      color: #34bfa3
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-icon {
      float: left;
      font-size: 48px;
    }

    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px;
      margin-left: 0px;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }

      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}

@media (max-width:550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>
