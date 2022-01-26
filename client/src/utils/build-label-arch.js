import store from '@/store'

export function buildLabelArch(data) {
  var nodeMapper = {}
  var nodeData = null
  data.forEach(e => {
    // if (nodeMapper.hasOwnProperty(e['parent_id'])) {
    if (Object.prototype.hasOwnProperty.call(nodeMapper, e['parent_id'])) {
      nodeMapper[e['parent_id']].push(e)
    } else {
      nodeMapper[e['parent_id']] = [e]
    }
  })
  nodeData = buildHelper(nodeMapper['nan'][0], nodeMapper, 1)
  return nodeData
}

export function buildStockLabels(arch, labels) {
  var nodeMapper = {}
  var nodeData = null
  arch.forEach(e => {
    // if (nodeMapper.hasOwnProperty(e['parent_id'])) {
    if (Object.prototype.hasOwnProperty.call(nodeMapper, e['parent_id'])) {
      nodeMapper[e['parent_id']].push(e)
    } else {
      nodeMapper[e['parent_id']] = [e]
    }
  })
  labels.forEach(e => {
    if (Object.prototype.hasOwnProperty.call(nodeMapper, e['label_id'])) {
      nodeMapper[e['label_id']].push({ label_id: e['id'], label_name: e['value'] })
    } else {
      nodeMapper[e['label_id']] = [{ label_id: e['id'], label_name: e['value'] }]
    }
  })
  // console.log(store.getters)
  if (typeof labels[0] !== 'undefined') {
    // 设置根节点的显示为股票代码
    // console.log(labels[0])
    for (const stk of JSON.parse(localStorage.getItem('stock_list'))) {
        if (stk.code === labels[0].asset_id) {
            nodeMapper['nan'][0].label_name = stk.name
            break
        }
    }
  }
  nodeData = buildHelper(nodeMapper['nan'][0], nodeMapper, 1)
  return nodeData
}

export function buildHelper(cur, nodeMapper, level) {
  var nodeData = {}
  nodeData['id'] = cur.label_id
  nodeData['topic'] = cur.label_name
  if (level <= 3) {
    nodeData['expanded'] = true
  } else {
    nodeData['expanded'] = false
  }
  if (cur.parent_id === 'nan') {
    nodeData['root'] = true
  }
  // if (nodeMapper.hasOwnProperty(cur.label_id)) {
  if (Object.prototype.hasOwnProperty.call(nodeMapper, cur.label_id)) {
    nodeData['children'] = []
    nodeMapper[cur.label_id].forEach(e => {
      nodeData['children'].push(buildHelper(e, nodeMapper, level + 1))
    })
  }
  return nodeData
}
