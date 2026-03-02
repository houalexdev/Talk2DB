<script lang="ts">
    import Text from "./Text.svelte";

    export let marked_correct: boolean;
</script>

<Text>结果正确吗？</Text>

<div class="flex items-center">
    <span class="text-sm text-gray-500 mr-3 dark:text-gray-400">不正确</span>
    <input type="checkbox" bind:checked={marked_correct} class="relative shrink-0 w-[3.25rem] h-7 bg-gray-100 checked:bg-none checked:bg-blue-600 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 border border-transparent ring-1 ring-transparent focus:border-blue-600 focus:ring-blue-600 ring-offset-white focus:outline-none appearance-none dark:bg-gray-700 dark:checked:bg-blue-600 dark:focus:ring-offset-gray-800
  
    before:inline-block before:w-6 before:h-6 before:bg-white checked:before:bg-blue-200 before:translate-x-0 checked:before:translate-x-full before:shadow before:rounded-full before:transform before:ring-0 before:transition before:ease-in-out before:duration-200 dark:before:bg-gray-400 dark:checked:before:bg-blue-200">
    <span class="text-sm text-gray-500 ml-3 dark:text-gray-400">正确</span>
</div>