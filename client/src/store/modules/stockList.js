import { fetchStockList } from '@/api/stock'

const state = {
  stock_list: []
}

const mutations = {
  SET_STOCK_LIST: (state, stocks) => {
    state.stock_list = stocks
  },
  ADD_STOCK: (state, stock) => {
    state.stock_list.push(stock)
  }
}

const actions = {
  // fetch stock list
  fetchStockList({ commit, state }) {
    return new Promise((resolve, reject) => {
      fetchStockList().then(response => {
        const { data } = response
        commit('SET_STOCK_LIST', data)
        // 保存股票列表到localStorage
        window.localStorage.setItem('stock_list', JSON.stringify(data))
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
