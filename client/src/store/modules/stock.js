import { getStockLabels } from '@/api/label-arch'

const state = {
  stock_labels: []
}

const mutations = {
  SET_STOCK_LABELS: (state, labels) => {
    state.stock_labels = labels
  },
  ADD_STOCK_LABEL: (state, label) => {
    state.stock_labels.push(label)
  }
}

const actions = {
  // fetch stock label
  fetchStockLabels({ commit, state }, val) {
    return new Promise((resolve, reject) => {
      getStockLabels(undefined, val.code, undefined).then(response => {
        const { data } = response
        commit('SET_STOCK_LABELS', data)
        // 保存股票标签到localStorage
        window.localStorage.setItem('stock_labels', JSON.stringify(data))
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
