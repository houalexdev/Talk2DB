<script lang="ts">
    export let message: string;
    export let onSubmit: (message: string) => void; // 提交时将调用的回调函数

    function handleClick() {
        onSubmit(message);
    }
</script>

<button type="button" on:click={handleClick} class="mb-2.5 mr-1.5 py-3 px-4 inline-flex justify-center items-center gap-2 rounded-md border-2 border-green-200 font-semibold text-green-500 hover:text-white hover:bg-green-500 hover:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-200 focus:ring-offset-2 transition-all text-sm dark:focus:ring-offset-gray-800">
    {message}
</button>