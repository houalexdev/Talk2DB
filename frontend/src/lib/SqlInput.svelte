<script lang="ts">
    import InChatButton from "./InChatButton.svelte";

    export let onSubmit: (sql: string) => void; // a callback function that will be called on Submit

    let sql: string;
</script>

<textarea bind:value={sql} class="block p-2.5 w-full text-blue-600 hover:text-blue-500 text-2xl dark:text-blue-500 dark:hover:text-blue-400 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 font-mono" placeholder="SELECT col1, col2, col3 FROM ..."></textarea>

<InChatButton message="训练" onSubmit={() => onSubmit(sql)} />