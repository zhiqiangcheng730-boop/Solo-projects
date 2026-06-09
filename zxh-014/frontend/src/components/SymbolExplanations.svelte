<script>
  import { createEventDispatcher } from "svelte";
  import { userId } from "../lib/stores.js";

  export let symbol;

  const dispatch = createEventDispatcher();

  let explanations = [];
  let newExplanation = "";
  let loading = false;

  $: if (symbol) loadExplanations();

  async function loadExplanations() {
    if (!symbol) return;
    loading = true;
    try {
      const { api } = await import("../lib/api.js");
      const data = await api.getExplanations(symbol.id);
      explanations = data.map((e) => ({
        ...e,
        vote_count: e.vote_count ?? (e.votes ? e.votes.length : 0),
      }));
      explanations.sort((a, b) => b.vote_count - a.vote_count);
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
  }

  async function submitExplanation() {
    if (!newExplanation.trim() || !symbol) return;
    const { api } = await import("../lib/api.js");
    await api.addExplanation({
      symbol_id: symbol.id,
      explanation: newExplanation.trim(),
      user_id: $userId,
    });
    newExplanation = "";
    loadExplanations();
  }

  async function toggleVote(exp) {
    const { api } = await import("../lib/api.js");
    const result = await api.voteExplanation({
      explanation_id: exp.id,
      user_id: $userId,
    });
    loadExplanations();
  }
</script>

<div class="bg-white rounded-xl shadow p-6">
  {#if !symbol}
    <p class="text-gray-400 text-sm text-center py-8">选择一个符号查看解释</p>
  {:else}
    <h3 class="text-lg font-semibold text-gray-800 mb-2">「{symbol.keyword}」的解释</h3>
    <p class="text-sm text-gray-500 mb-4">{symbol.description || "暂无系统描述"}</p>

    <div class="mb-4 flex gap-2">
      <input
        type="text"
        bind:value={newExplanation}
        placeholder="分享你对这个符号的理解..."
        class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-400 focus:border-transparent"
      />
      <button
        class="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-indigo-700 transition-colors whitespace-nowrap"
        disabled={!newExplanation.trim()}
        on:click={submitExplanation}
      >
        提交
      </button>
    </div>

    {#if loading}
      <p class="text-gray-400 text-sm text-center py-4">加载中...</p>
    {:else if explanations.length === 0}
      <p class="text-gray-400 text-sm text-center py-4">暂无解释，成为第一个解读的人吧</p>
    {:else}
      <div class="space-y-3 max-h-80 overflow-y-auto">
        {#each explanations as exp}
          <div class="border border-gray-100 rounded-lg p-3">
            <p class="text-sm text-gray-700">{exp.explanation}</p>
            <div class="mt-2 flex items-center gap-3 text-xs text-gray-400">
              <span>{exp.user_id}</span>
              <button
                class="flex items-center gap-1 text-indigo-500 hover:text-indigo-700"
                on:click={() => toggleVote(exp)}
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                </svg>
                {exp.vote_count}
              </button>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  {/if}
</div>
