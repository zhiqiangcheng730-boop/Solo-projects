<script>
  import { onMount } from "svelte";
  import { userId } from "../lib/stores.js";
  import { api } from "../lib/api.js";
  import DreamForm from "../components/DreamForm.svelte";
  import WordCloud from "../components/WordCloud.svelte";
  import AnonymousShare from "../components/AnonymousShare.svelte";

  let dreams = [];
  let selectedDream = null;
  let topKeywords = [];
  let shareUrl = "";
  let formRef;

  onMount(loadDreams);

  async function loadDreams() {
    try {
      dreams = await api.listDreams($userId);
      if (dreams.length > 0 && !selectedDream) {
        selectedDream = dreams[0];
      }
      const stats = await api.getOverview();
      topKeywords = stats.top_keywords || [];
    } catch (e) {
      console.error(e);
    }
  }

  async function handleSubmit(event) {
    try {
      await api.createDream({
        content: event.detail.content,
        emotion: event.detail.emotion,
        user_id: $userId,
      });
      formRef.reset();
      loadDreams();
    } catch (e) {
      alert("提交失败：" + e.message);
    }
  }

  async function handleShare(event) {
    try {
      const share = await api.createShare(event.detail);
      shareUrl = `${window.location.origin}/#/share/${share.share_token}`;
    } catch (e) {
      alert("分享失败：" + e.message);
    }
  }

  function selectDream(dream) {
    selectedDream = dream;
    shareUrl = "";
  }
</script>

<div class="space-y-6">
  <h2 class="text-2xl font-bold text-gray-800">记录梦境</h2>

  <div class="grid md:grid-cols-3 gap-6">
    <div class="md:col-span-2 space-y-6">
      <DreamForm bind:this={formRef} on:submit={handleSubmit} />

      <div class="bg-white rounded-xl shadow p-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">我的梦境记录</h3>
        {#if dreams.length === 0}
          <p class="text-gray-400 text-sm text-center py-8">还没有记录任何梦境</p>
        {:else}
          <div class="space-y-2 max-h-96 overflow-y-auto">
            {#each dreams as dream}
              <button
                class="w-full text-left p-3 rounded-lg border transition-colors"
                class:border-indigo-300={selectedDream?.id === dream.id}
                class:bg-indigo-50={selectedDream?.id === dream.id}
                class:border-gray-200={selectedDream?.id !== dream.id}
                class:hover:bg-gray-50={selectedDream?.id !== dream.id}
                on:click={() => selectDream(dream)}
              >
                <p class="text-sm text-gray-700 line-clamp-2">{dream.content}</p>
                <div class="mt-1 flex items-center gap-2 text-xs text-gray-400">
                  <span>{new Date(dream.created_at).toLocaleDateString("zh-CN")}</span>
                  {#if dream.emotion}
                    <span class="text-indigo-500">{dream.emotion}</span>
                  {/if}
                  {#if dream.keywords?.length}
                    <span>{dream.keywords.map(k => k.keyword).join("、")}</span>
                  {/if}
                </div>
              </button>
            {/each}
          </div>
        {/if}
      </div>
    </div>

    <div class="space-y-6">
      <AnonymousShare dream={selectedDream} on:share={handleShare} bind:shareUrl />
      {#if shareUrl}
        <div class="bg-green-50 border border-green-200 rounded-lg p-3 text-xs text-green-800">
          分享链接已生成！可前往「匿名社区」查看
        </div>
      {/if}
    </div>
  </div>
</div>
