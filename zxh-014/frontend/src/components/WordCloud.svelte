<script>
  import { onMount, afterUpdate } from "svelte";
  import { renderWordCloud } from "../lib/wordcloud.js";

  export let words = [];
  let canvas;
  let rendered = false;

  $: if (words.length > 0 && canvas) {
    renderWordCloud(canvas, words);
  }
</script>

<div class="bg-white rounded-xl shadow p-6">
  <h3 class="text-lg font-semibold text-gray-800 mb-4">梦境符号云图</h3>
  {#if words.length === 0}
    <p class="text-gray-400 text-sm text-center py-12">暂无数据，记录梦境后符号将在此展示</p>
  {:else}
    <canvas bind:this={canvas} class="w-full"></canvas>
  {/if}
</div>
