import request from '@/utils/request'

export function fetchStockList() {
  return request({
    url: '/stock/stock_list',
    method: 'get'
  })
}
