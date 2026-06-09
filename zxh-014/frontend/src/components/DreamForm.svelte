<script>
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  let content = "";
  let emotion = null;
  let submitting = false;

  const emotions = [
    { value: "anxiety", label: "焦虑", color: "bg-orange-100 border-orange-400 text-orange-700" },
    { value: "calm", label: "平静", color: "bg-green-100 border-green-400 text-green-700" },
    { value: "excited", label: "兴奋", color: "bg-purple-100 border-purple-400 text-purple-700" },
  ];

  function selectEmotion(val) {
    emotion = emotion === val ? null : val;
  }

  async function handleSubmit() {
    if (!content.trim()) return;
    submitting = true;
    dispatch("submit", { content: content.trim(), emotion });
  }

  export function reset() {
    content = "";
    emotion = null;
    submitting = false;
  }
</script>

<div class="bg-white rounded-xl shadow p-6">
  <h3 class="text-lg font-semibold text-gray-800 mb-4">记录你的梦境</h3>
  <textarea
    bind:value={content}
    rows="5"
    class="w-full border border-gray-300 rounded-lg p-3 text-sm focus:ring-2 focus:ring-indigo-400 focus:border-transparent resize-none"
    placeholder="描述你昨晚的梦境..."
  ></textarea>

  <div class="mt-3 flex flex-wrap gap-2 items-center">
    <span class="text-sm text-gray-500 mr-1">当前情绪：</span>
    {#each emotions as em}
      <button
        class="px-3 py-1 rounded-full text-sm border {em.color}"
        class:ring-2={emotion === em.value}
        class:ring-indigo-400={emotion === em.value}
        on:click={() => selectEmotion(em.value)}
      >
        {em.label}
      </button>
    {/each}
  </div>

  <button
    class="mt-4 w-full bg-indigo-600 text-white py-2.5 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50 transition-colors"
    disabled={!content.trim() || submitting}
    on:click={handleSubmit}
  >
    {submitting ? "提交中..." : "记录梦境"}
  </button>
</div>
