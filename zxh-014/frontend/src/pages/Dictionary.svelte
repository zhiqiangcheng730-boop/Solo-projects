<script>
  import { onMount } from "svelte";
  import { api } from "../lib/api.js";
  import WordCloud from "../components/WordCloud.svelte";
  import SymbolExplanations from "../components/SymbolExplanations.svelte";

  let symbols = [];
  let topKeywords = [];
  let selectedSymbol = null;
  let search = "";
  let loading = true;

  $: filteredSymbols = search
    ? symbols.filter((s) => s.keyword.includes(search))
    : symbols;

  onMount(async () => {
    try {
      [symbols, { top_keywords }] = await Promise.all([
        api.listSymbols(),
        api.getTopKeywords(),
      ]);
      topKeywords = top_keywords;
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
  });

  function selectSymbol(sym) {
    selectedSymbol = sym;
  }
</script>

<div class="space-y-6">
  <h2 class="text-2xl font-bold text-gray-800">符号词典</h2>

  <WordCloud words={topKeywords} />

  <div class="grid md:grid-cols-3 gap-6">
    <div class="bg-white rounded-xl shadow p-6">
      <div class="mb-4">
        <input
          type="text"
          bind:value={search}
          placeholder="搜索符号..."
          class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-400 focus:border-transparent"
        />
      </div>

      {#if loading}
        <p class="text-gray-400 text-sm text-center py-4">加载中...</p>
      {:else}
        <div class="flex flex-wrap gap-1.5 max-h-96 overflow-y-auto">
          {#each filteredSymbols as sym}
            <button
              class="px-2.5 py-1 rounded-full text-xs border transition-colors"
              class:bg-indigo-600={selectedSymbol?.id === sym.id}
              class:text-white={selectedSymbol?.id === sym.id}
              class:border-indigo-600={selectedSymbol?.id === sym.id}
              class:border-gray-300={selectedSymbol?.id !== sym.id}
              class:hover:border-indigo-400={selectedSymbol?.id !== sym.id}
              class:text-gray-600={selectedSymbol?.id !== sym.id}
              on:click={() => selectSymbol(sym)}
            >
              {sym.keyword}
            </button>
          {/each}
        </div>
      {/if}
    </div>

    <div class="md:col-span-2">
      <SymbolExplanations symbol={selectedSymbol} />
    </div>
  </div>
</div>
