<script>
  import { onMount } from "svelte";
  import { api } from "../lib/api.js";

  let correlations = [];
  let selectedEmotion = null;
  let loading = true;

  const emotionLabels = {
    anxiety: "焦虑",
    calm: "平静",
    excited: "兴奋",
  };

  const emotionColors = {
    anxiety: "border-orange-400 bg-orange-50",
    calm: "border-green-400 bg-green-50",
    excited: "border-purple-400 bg-purple-50",
  };

  onMount(async () => {
    try {
      correlations = await api.getEmotionCorrelation();
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
  });
</script>

<div class="bg-white rounded-xl shadow p-6">
  <h3 class="text-lg font-semibold text-gray-800 mb-4">情绪与梦境符号关联</h3>

  {#if loading}
    <p class="text-gray-400 text-sm text-center py-8">加载中...</p>
  {:else if correlations.length === 0}
    <p class="text-gray-400 text-sm text-center py-8">暂无情绪数据</p>
  {:else}
    <div class="flex flex-wrap gap-2 mb-4">
      {#each correlations as corr}
        <button
          class="px-3 py-1 rounded-full text-sm border {emotionColors[corr.emotion] ?? ''}"
          class:ring-2={selectedEmotion === corr.emotion}
          class:ring-indigo-400={selectedEmotion === corr.emotion}
          on:click={() => selectedEmotion = selectedEmotion === corr.emotion ? null : corr.emotion}
        >
          {emotionLabels[corr.emotion] ?? corr.emotion} ({corr.dream_count}条)
        </button>
      {/each}
    </div>

    {#each correlations.filter(c => !selectedEmotion || c.emotion === selectedEmotion) as corr}
      <div class="mb-4">
        <h4 class="text-sm font-medium text-gray-700 mb-2">
          {emotionLabels[corr.emotion] ?? corr.emotion} 人群高频梦境符号
        </h4>
        {#if corr.top_keywords.length === 0}
          <p class="text-gray-400 text-sm">暂无数据</p>
        {:else}
          <div class="flex flex-wrap gap-1.5">
            {#each corr.top_keywords as kw}
              <span class="inline-flex items-center gap-1 px-2 py-0.5 bg-gray-100 rounded text-xs">
                <span class="font-medium">{kw.keyword}</span>
                <span class="text-gray-400">
                  ({kw.emotion_ratio}%)
                </span>
                {#if kw.emotion_ratio > kw.global_ratio}
                  <span class="text-red-500 text-[10px]">↑</span>
                {/if}
              </span>
            {/each}
          </div>
        {/if}
      </div>
    {/each}
  {/if}
</div>
