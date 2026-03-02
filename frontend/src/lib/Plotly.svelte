<script lang="ts">
    import { onMount } from "svelte";

    export let fig: string;

    let figJson = JSON.parse(fig);

    // 为div id生成一个UUID
    let id = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);

    onMount(() => {
        Plotly.newPlot( document.getElementById(id), figJson, {responsive: true} )
    });
</script>

<div id={id}></div>