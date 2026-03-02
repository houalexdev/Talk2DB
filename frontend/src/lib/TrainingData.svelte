<script lang="ts">
    import Text from "./Text.svelte";
    import type { MessageContents } from "./types";
    import TrainingDataFrame from "./TrainingDataFrame.svelte";
    import Error from "./Error.svelte";

    export let trainingData: MessageContents | null;

    export let removeTrainingData: (id: string) => void;
    export let onTrain: (trainingData: string, trainingDataType: string) => void;
</script>

<div class="relative h-screen w-full lg:pl-64">
    <div class="py-10 lg:py-14">
        {#if trainingData !== null}
            {#if trainingData.type === 'df'}
                <TrainingDataFrame df={trainingData.df} removeTrainingData={removeTrainingData} onTrain={onTrain} />
            {:else if trainingData.type === 'error'}
                <Error message={trainingData.error} />
            {/if}
        {:else}
        <div class="min-h-[15rem] flex flex-col bg-white border shadow-sm rounded-xl dark:bg-gray-800 dark:border-gray-700 dark:shadow-slate-700/[.7]">
            <div class="flex flex-auto flex-col justify-center items-center p-4 md:p-5">
              <div class="flex justify-center">
                <div class="animate-spin inline-block w-6 h-6 border-[3px] border-current border-t-transparent text-blue-600 rounded-full" role="status" aria-label="loading">
                  <span class="sr-only">加载中...</span>
                </div>
              </div>
            </div>
          </div> 
        {/if}
    </div>
</div>