import request from '@/utils/request'

export function fetchIndicators(query) {
  return request({
    url: '/indicator',
    method: 'get',
    params: query
  })
}