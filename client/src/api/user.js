import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/auth/login',
    method: 'post',
    data
  })
}

export function getInfo(name) {
  return request({
    url: '/users/name/' + name,
    method: 'get'
  })
}

export function logout(data) {
  return request({
    url: '/auth/logout',
    method: 'post',
    data
  })
}
