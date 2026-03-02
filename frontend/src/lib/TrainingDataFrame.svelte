<script lang="ts">
    import ConfirmDelete from "./ConfirmDelete.svelte";
    import NewTrainingData from "./NewTrainingData.svelte";

    export let df;
    export let onTrain: (trainingData: string, trainingDataType: string) => void;
    export let removeTrainingData: (id: string) => void;
    let data = JSON.parse(df);

    // Extracting column names dynamically from the first record
    let columns = data.length > 0 ? Object.keys(data[0]) : [];

    let rowsPerPage = 10;

    let currentPage = 1;

    let totalPages = Math.ceil(data.length / rowsPerPage);

    let start = (currentPage - 1) * rowsPerPage;

    let end = currentPage * rowsPerPage;

    let paginatedData = data.slice(start, end);

    const prevPage = () => {
        if (currentPage > 1) {
            currentPage--;
        }
    };

    const nextPage = () => {
        if (currentPage < totalPages) {
            currentPage++;
        }
    };

    const viewAll = () => {
        currentPage = 1;
        rowsPerPage = data.length;
    };

    $: start = (currentPage - 1) * rowsPerPage;

    $: end = currentPage * rowsPerPage;

    $: paginatedData = data.slice(start, end);

    $: totalPages = Math.ceil(data.length / rowsPerPage);

    $: console.log(currentPage, totalPages);
    
    let confirmDelete: string | null = null;
    let addingTrainingData: boolean = false;

    const addTrainingData = () => {
        addingTrainingData = true;
    }

    const dismissAddingTrainingData = () => {
        addingTrainingData = false;
    }
</script>

{#if addingTrainingData}
    <NewTrainingData onDismiss={dismissAddingTrainingData} onTrain={onTrain} />
{/if}

<!-- Table Section -->
<div class="max-w-[85rem] px-4 py-10 sm:px-6 lg:px-8 lg:py-14 mx-auto">
    <!-- Card -->
    <div class="flex flex-col">
      <div class="-m-1.5 overflow-x-auto">
        <div class="p-1.5 min-w-full inline-block align-middle">
          <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden dark:bg-slate-900 dark:border-gray-700">
            <!-- Header -->
            <div class="px-6 py-4 grid gap-3 md:flex md:justify-between md:items-center border-b border-gray-200 dark:border-gray-700">
              <div>
                <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200">
                  训练数据
                </h2>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  添加或删除训练数据。优质的训练数据是确保准确性的关键。
                </p>
              </div>
  
              <div>
                <div class="inline-flex gap-x-2">
                  <button on:click={viewAll} class="py-2 px-3 inline-flex justify-center items-center gap-2 rounded-md border font-medium bg-white text-gray-700 shadow-sm align-middle hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-white focus:ring-blue-600 transition-all text-sm dark:bg-slate-900 dark:hover:bg-slate-800 dark:border-gray-700 dark:text-gray-400 dark:hover:text-white dark:focus:ring-offset-gray-800">
                    查看全部
                  </button>
  
                  <button on:click={addTrainingData} class="py-2 px-3 inline-flex justify-center items-center gap-2 rounded-md border border-transparent font-semibold bg-blue-500 text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all text-sm dark:focus:ring-offset-gray-800">
                    <svg class="w-3 h-3" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path d="M2.63452 7.50001L13.6345 7.5M8.13452 13V2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                    添加训练数据
                    </button>
                </div>
              </div>
            </div>
            <!-- End Header -->
  
            <!-- Table -->
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-slate-800">
                <tr>
                    {#each columns as column}
                        <th scope="col" class="px-6 py-3 text-left">
                            <div class="flex items-center gap-x-2">
                                <span class="text-xs font-semibold uppercase tracking-wide text-gray-800 dark:text-gray-200">
                                    {#if column != 'id'}
                                        {column}
                                    {:else}
                                        操作
                                    {/if}
                                </span>
                            </div>
                        </th>
                    {/each}
                </tr>                
              </thead>
  
              <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                {#each paginatedData as row}
                <tr>
                    {#each columns as column}
                        <td class="h-px w-px ">
                            <div class="px-6 py-3">
                                {#if column != 'id'}
                                    <span class="text-gray-800 dark:text-gray-200">{row[column]}</span>
                                {:else}
                                    <button type="button" on:click={() => {confirmDelete = row[column]}} class="py-2 px-3 inline-flex justify-center items-center gap-2 rounded-md border-2 border-red-200 font-semibold text-red-500 hover:text-white hover:bg-red-500 hover:border-red-500 focus:outline-none focus:ring-2 focus:ring-red-200 focus:ring-offset-2 transition-all text-sm dark:focus:ring-offset-gray-800">
                                        删除
                                    </button>
                                {/if}
                            </div>
                        </td>
                    {/each}
                </tr>
                {/each}                
              </tbody>
            </table>
            <!-- End Table -->
  
            <!-- Footer -->
            <div class="px-6 py-4 grid gap-3 md:flex md:justify-between md:items-center border-t border-gray-200 dark:border-gray-700">
                <div class="inline-flex items-center gap-x-2">
                    <p class="text-sm text-gray-600 dark:text-gray-400">
                        显示：
                    </p>
                    <div class="max-w-sm space-y-3">
                        <span class="py-2 px-3 pr-9 block w-full border-gray-200 rounded-md text-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400">
                            {start + 1} - { Math.min(end, data.length) }
                        </span>
                    </div>
                    <p class="text-sm text-gray-600 dark:text-gray-400">
                        共 {data.length} 条
                    </p>
                    </div>
  
              <div>
                <div class="inline-flex gap-x-2">
                  <button type="button" on:click={prevPage} class="py-2 px-3 inline-flex justify-center items-center gap-2 rounded-md border font-medium bg-white text-gray-700 shadow-sm align-middle hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-white focus:ring-blue-600 transition-all text-sm dark:bg-slate-900 dark:hover:bg-slate-800 dark:border-gray-700 dark:text-gray-400 dark:hover:text-white dark:focus:ring-offset-gray-800">
                    <svg class="w-3 h-3" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                      <path fill-rule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z"/>
                    </svg>
                    上一页
                  </button>
  
                  <button type="button" on:click={nextPage} class="py-2 px-3 inline-flex justify-center items-center gap-2 rounded-md border font-medium bg-white text-gray-700 shadow-sm align-middle hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-white focus:ring-blue-600 transition-all text-sm dark:bg-slate-900 dark:hover:bg-slate-800 dark:border-gray-700 dark:text-gray-400 dark:hover:text-white dark:focus:ring-offset-gray-800">
                    下一页
                    <svg class="w-3 h-3" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                      <path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            <!-- End Footer -->
          </div>
        </div>
      </div>
    </div>
    <!-- End Card -->
  </div>
  <!-- End Table Section -->

{#if confirmDelete != null}
    <ConfirmDelete message="您确定要删除此项吗？" buttonLabel="删除" onClose={() => {confirmDelete = null}} onConfirm={() => { if (confirmDelete) removeTrainingData(confirmDelete) }}  />
{/if}