<script lang="ts">
    export let message: string;
    export let onSubmit: (message: string) => void; // 提交时将调用的回调函数

    function handleClick() {
        onSubmit(message);
    }
</script>

<button type="button" on:click={handleClick} class="mb-2.5 mr-1.5 py-2 px-3 inline-flex justify-center items-center gap-x-2 rounded-md border border-blue-600 bg-white text-blue-600 align-middle hover:bg-blue-50 text-sm dark:bg-slate-900 dark:text-blue-500 dark:border-blue-500 dark:hover:text-blue-400 dark:hover:border-blue-400">
    {message}
</button>