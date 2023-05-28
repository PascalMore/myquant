import request from '@/utils/request'

export function fetchIndexYields(query) {
  return request({
    url: '/index/yield',
    method: 'get',
    params: query
  })
}
