import request from '@/utils/request'

export function fetchAllStrategyExecutions() {
  return request({
    url: '/strategy/execution/list',
    method: 'get'
  })
}

export function fetchStrategyExecutions(query) {
  return request({
    url: '/strategy/execution',
    method: 'get',
    params: query
  })
}
