<template>
  <div id="app">
    <div id="map" style="width:100%;height:630px"></div>
  </div>
</template>

<script>
import MindElixir, { E } from "mind-elixir"

export default {
  name: "StockData",
  data() {
    return {
      ME: null
    };
  },
  mounted() {
    this.ME = new MindElixir({
      el: "#map",
      direction: MindElixir.LEFT,
      data: MindElixir.example,
      draggable: true, // default true
      contextMenu: true, // default true
      toolBar: true, // default true
      nodeMenu: true, // default true
      keypress: true // default true
    });
    this.ME.init();
    this.ME.example();
  }
};
</script>

<style>
</style>
