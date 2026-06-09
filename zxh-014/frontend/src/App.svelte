<script>
  import { currentPage, userId } from "./lib/stores.js";
  import Home from "./pages/Home.svelte";
  import Record from "./pages/Record.svelte";
  import Dictionary from "./pages/Dictionary.svelte";
  import Trends from "./pages/Trends.svelte";
  import Community from "./pages/Community.svelte";

  const navItems = [
    { id: "home", label: "首页" },
    { id: "record", label: "记录梦境" },
    { id: "dictionary", label: "符号词典" },
    { id: "trends", label: "趋势分析" },
    { id: "community", label: "匿名社区" },
  ];
</script>

<div class="min-h-screen flex flex-col">
  <nav class="bg-indigo-700 text-white shadow-lg sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 py-3 flex items-center gap-6">
      <span class="text-xl font-bold tracking-wide">梦境符号词典</span>
      <div class="flex gap-1">
        {#each navItems as item}
          <button
            class="px-3 py-1.5 rounded text-sm transition-colors"
            class:bg-indigo-500={$currentPage === item.id}
            class:hover:bg-indigo-600={$currentPage !== item.id}
            on:click={() => currentPage.set(item.id)}
          >
            {item.label}
          </button>
        {/each}
      </div>
      <span class="ml-auto text-xs text-indigo-200">ID: {$userId}</span>
    </div>
  </nav>

  <main class="flex-1 max-w-6xl mx-auto w-full px-4 py-6">
    {#if $currentPage === "home"}
      <Home />
    {:else if $currentPage === "record"}
      <Record />
    {:else if $currentPage === "dictionary"}
      <Dictionary />
    {:else if $currentPage === "trends"}
      <Trends />
    {:else if $currentPage === "community"}
      <Community />
    {/if}
  </main>
</div>
