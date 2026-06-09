<script>
  import { onMount } from "svelte";
  import { currentPage } from "../lib/stores.js";
  import { api } from "../lib/api.js";
  import StatsPanel from "../components/StatsPanel.svelte";
  import WordCloud from "../components/WordCloud.svelte";

  let stats = null;
  let topKeywords = [];
  let topExplanations = [];
  let loading = true;

  onMount(async () => {
    try {
      stats = await api.getOverview();
      topKeywords = stats.top_keywords || [];
      topExplanations = stats.top_explanations || [];
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
  });
</script>

<div class="space-y-6">
  <div class="text-center py-4">
    <h1 class="text-3xl font-bold text-gray-800">梦境符号词典</h1>
    <p class="text-gray-500 mt-2">记录梦境 · 探索符号 · 理解自我</p>
  </div>

  <StatsPanel {stats} />

  <div class="grid md:grid-cols-2 gap-6">
    <WordCloud words={topKeywords} />
    <div class="bg-white rounded-xl shadow p-6">
      <h3 class="text-lg font-semibold text-gray-800 mb-4">最受认可的符号解读</h3>
      {#if loading}
        <p class="text-gray-400 text-sm text-center py-8">加载中...</p>
      {:else if topExplanations.length === 0}
        <p class="text-gray-400 text-sm text-center py-8">暂无解读数据</p>
      {:else}
        <div class="space-y-3 max-h-80 overflow-y-auto">
          {#each topExplanations as exp}
            <div class="border-b border-gray-100 pb-2 last:border-0">
              <div class="flex items-center gap-2">
                <span class="text-xs font-medium bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded">
                  {exp.keyword}
                </span>
                <span class="text-xs text-gray-400">{exp.vote_count}赞</span>
              </div>
              <p class="text-sm text-gray-600 mt-1">{exp.explanation}</p>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  </div>

  <div class="text-center">
    <button
      class="bg-indigo-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-indigo-700 transition-colors"
      on:click={() => currentPage.set("record")}
    >
      开始记录你的梦境
    </button>
  </div>
</div>
