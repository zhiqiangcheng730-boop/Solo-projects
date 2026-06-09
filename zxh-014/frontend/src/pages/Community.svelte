<script>
  import { onMount } from "svelte";
  import { api } from "../lib/api.js";
  import DreamFeed from "../components/DreamFeed.svelte";

  let shares = [];
  let loading = true;

  onMount(async () => {
    try {
      shares = await api.listShares();
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
  });
</script>

<div class="space-y-6">
  <div>
    <h2 class="text-2xl font-bold text-gray-800">匿名社区</h2>
    <p class="text-gray-500 text-sm mt-1">
      这里展示所有匿名分享的梦境，你可以留言为陌生人解读梦境。所有内容均为匿名。
    </p>
  </div>
  <DreamFeed {shares} {loading} />
</div>
