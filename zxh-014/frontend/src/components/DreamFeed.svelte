<script>
  import { userId } from "../lib/stores.js";

  export let shares = [];
  export let loading = false;

  let commentInputs = {};
  let expanded = {};

  function toggleExpand(id) {
    expanded[id] = !expanded[id];
    expanded = expanded;
  }

  export async function handleComment(shareId, content) {
    const { api } = await import("../lib/api.js");
    await api.addComment(shareId, { user_id: $userId, content });
  }
</script>

<div class="space-y-4">
  {#if loading}
    <p class="text-gray-400 text-sm text-center py-8">加载中...</p>
  {:else if shares.length === 0}
    <p class="text-gray-400 text-sm text-center py-8">暂无匿名分享</p>
  {:else}
    {#each shares as share}
      <div class="bg-white rounded-xl shadow p-5">
        <p class="text-sm text-gray-700 leading-relaxed">{share.dream_content}</p>
        {#if share.dream_emotion}
          <span class="inline-block mt-2 text-xs bg-indigo-50 text-indigo-600 px-2 py-0.5 rounded">
            {share.dream_emotion}
          </span>
        {/if}
        <div class="mt-3 flex items-center justify-between text-xs text-gray-400">
          <span>{new Date(share.created_at).toLocaleDateString("zh-CN")}</span>
          <button
            class="text-indigo-500 hover:text-indigo-700"
            on:click={() => toggleExpand(share.id)}
          >
            留言 ({share.comment_count})
          </button>
        </div>

        {#if expanded[share.id]}
          <div class="mt-3 border-t pt-3">
            <!-- comments would load here -->
            <div class="flex gap-2 mt-2">
              <input
                type="text"
                bind:value={commentInputs[share.id]}
                placeholder="写下你的解读..."
                class="flex-1 border border-gray-200 rounded px-2 py-1 text-xs"
              />
              <button
                class="bg-indigo-600 text-white px-3 py-1 rounded text-xs hover:bg-indigo-700"
                on:click={() => {
                  if (commentInputs[share.id]?.trim()) {
                    handleComment(share.id, commentInputs[share.id]);
                    commentInputs[share.id] = "";
                    share.comment_count += 1;
                  }
                }}
              >
                发送
              </button>
            </div>
          </div>
        {/if}
      </div>
    {/each}
  {/if}
</div>
