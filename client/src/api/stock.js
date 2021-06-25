import request from '@/utils/request'

export function fetchStockList() {
  return request({
    url: '/stock_list',
    method: 'get'
  })
}
