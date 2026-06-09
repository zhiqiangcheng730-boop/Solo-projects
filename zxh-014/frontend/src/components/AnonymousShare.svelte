<script>
  import { createEventDispatcher } from "svelte";

  export let dream = null;
  export let shareUrl = "";
  const dispatch = createEventDispatcher();

  let copied = false;

  async function handleShare() {
    if (!dream) return;
    dispatch("share", dream.id);
  }

  function copyLink() {
    if (!shareUrl) return;
    navigator.clipboard.writeText(shareUrl).then(() => {
      copied = true;
      setTimeout(() => (copied = false), 2000);
    });
  }
</script>

<div class="bg-white rounded-xl shadow p-6">
  <h3 class="text-lg font-semibold text-gray-800 mb-4">匿名分享梦境</h3>
  {#if !dream}
    <p class="text-gray-400 text-sm text-center py-8">选择一个梦境进行匿名分享</p>
  {:else}
    <div class="bg-gray-50 rounded-lg p-4 mb-4">
      <p class="text-sm text-gray-700 line-clamp-4">{dream.content}</p>
      {#if dream.emotion}
        <span class="inline-block mt-2 text-xs text-indigo-500">情绪：{dream.emotion}</span>
      {/if}
    </div>
    {#if !shareUrl}
      <button
        class="w-full bg-indigo-600 text-white py-2.5 rounded-lg text-sm hover:bg-indigo-700 transition-colors"
        on:click={handleShare}
      >
        匿名分享此梦境
      </button>
    {:else}
      <div class="flex gap-2 items-center">
        <input
          type="text"
          value={shareUrl}
          readonly
          class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-xs bg-gray-50"
        />
        <button
          class="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-indigo-700 transition-colors whitespace-nowrap"
          on:click={copyLink}
        >
          {copied ? "已复制" : "复制链接"}
        </button>
      </div>
    {/if}
  {/if}
</div>
