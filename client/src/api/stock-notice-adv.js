import request from '@/utils/request'

export function fetchStockNoticeAdv(query) {
  return request({
    url: '/stock_notice_adv',
    method: 'get',
    params: query
  })
}
