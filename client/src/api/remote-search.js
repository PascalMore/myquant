import request from '@/utils/request'

export function searchUser(name) {
  return request({
    url: '/users/name/'+name,
    method: 'get'
  })
}

export function transactionList(query) {
  return request({
    url: '/vue-element-admin/transaction/list',
    method: 'get',
    params: query
  })
}
