<script lang="ts">
    import DownloadButton from "./DownloadButton.svelte";

    export let id: string;
    export let df;
    export let config: any; // 添加config参数
    let data = JSON.parse(df);

    // 从第一条记录中动态提取列名
    let columns = data.length > 0 ? Object.keys(data[0]) : [];
</script>

<!-- 创建动态表格 -->
<div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden dark:bg-slate-900 dark:border-gray-700">

<div class="-m-1.5 overflow-x-auto">
<div class="p-1.5 min-w-full inline-block align-middle">    
<table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
    <thead class="bg-gray-50 dark:bg-slate-800">
        <tr>
            {#each columns as column}
                <th scope="col" class="px-6 py-3 text-left">
                    <div class="flex items-center gap-x-2">
                        <span class="text-xs font-semibold uppercase tracking-wide text-gray-800 dark:text-gray-200">
                            {column}
                        </span>
                    </div>
                </th>
            {/each}
        </tr>
    </thead>
    <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
        {#each data as row}
            <tr>
                {#each columns as column}
                    <td class="h-px w-px whitespace-nowrap">
                        <div class="px-6 py-3">
                            <span class="text-gray-800 dark:text-gray-200">{row[column]}</span>
                        </div>
                    </td>
                {/each}
            </tr>
        {/each}
    </tbody>
</table>
</div>
</div>

</div>

<!-- 根据配置显示或隐藏下载按钮 -->
{#if config && config.csv_download !== false}
  <DownloadButton id={id} />
{/if}
