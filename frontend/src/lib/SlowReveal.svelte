<script lang="ts">
    export let text;
    let words = text.split(' ');
    let currentIndex = 0;
  
    const revealNextWord = () => {
      if (currentIndex < words.length) {
        currentIndex++;
      }
    };
  
    setInterval(revealNextWord, 100); // Change 1000 to the desired interval in milliseconds
  </script>
  
{#each words as word, index}
    <span class={index < currentIndex ? 'inline' : 'hidden'}>{word}</span>
    {#if index < currentIndex}<span class="inline"> </span>{/if}
{/each}
  