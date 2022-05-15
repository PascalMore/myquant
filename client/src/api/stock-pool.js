import request from '@/utils/request'

export function fetchStockPool(query) {
  return request({
    url: '/stock_pool',
    method: 'get',
    params: query
  })
}
