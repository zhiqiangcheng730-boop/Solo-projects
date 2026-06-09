<script>
  export let stats = null;
</script>

<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
  <div class="bg-white rounded-xl shadow p-4 text-center">
    <p class="text-2xl font-bold text-indigo-600">{stats?.total_dreams ?? 0}</p>
    <p class="text-xs text-gray-500 mt-1">已记录梦境</p>
  </div>
  <div class="bg-white rounded-xl shadow p-4 text-center">
    <p class="text-2xl font-bold text-green-600">{stats?.total_symbols ?? 0}</p>
    <p class="text-xs text-gray-500 mt-1">梦境符号</p>
  </div>
  <div class="bg-white rounded-xl shadow p-4 text-center">
    <p class="text-2xl font-bold text-purple-600">{stats?.total_explanations ?? 0}</p>
    <p class="text-xs text-gray-500 mt-1">用户解读</p>
  </div>
  <div class="bg-white rounded-xl shadow p-4 text-center">
    <p class="text-2xl font-bold text-amber-600">{stats?.total_shares ?? 0}</p>
    <p class="text-xs text-gray-500 mt-1">匿名分享</p>
  </div>
</div>
