<script lang="ts">
    import { onMount } from 'svelte';
    import type { ApiData, MessageContents } from './types.ts';

    export let endpoint: string;
    export let question: string;
    let apiStatus: ApiData<MessageContents> = { status: 'NotRequested' };
  
    onMount(async () => {
      try {
        apiStatus = { status: 'Loading' };
        const response = await fetch(`/api/v1/${endpoint}?question=${question}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data: MessageContents = await response.json();
        apiStatus = { status: 'Loaded', data };
      } catch (error) {
        apiStatus = { status: 'Error', error: "Put the error here" };
      }
    });
  </script>

{#if apiStatus.status === 'NotRequested'}
  <p>数据尚未请求。</p>
{:else if apiStatus.status === 'Loading'}
<li class="max-w-4xl py-2 px-4 sm:px-6 lg:px-8 mx-auto flex gap-x-2 sm:gap-x-4">
    <svg class="flex-shrink-0 w-[2.375rem] h-[2.375rem] rounded-full animate-bounce" width="38" height="38" viewBox="0 0 38 38" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="38" height="38" rx="6" fill="#2563EB"/>
        <path d="M10 28V18.64C10 13.8683 14.0294 10 19 10C23.9706 10 28 13.8683 28 18.64C28 23.4117 23.9706 27.28 19 27.28H18.25" stroke="white" stroke-width="1.5"/>
        <path d="M13 28V18.7552C13 15.5104 15.6863 12.88 19 12.88C22.3137 12.88 25 15.5104 25 18.7552C25 22 22.3137 24.6304 19 24.6304H18.25" stroke="white" stroke-width="1.5"/>
        <ellipse cx="19" cy="18.6554" rx="3.75" ry="3.6" fill="white"/>
    </svg>
    
    <div class="space-y-3">
        <h2 class="font-medium text-gray-800 dark:text-white">
        加载中...
        </h2>
    </div>
</li>
{:else if apiStatus.status === 'Loaded'}
<li class="max-w-4xl py-2 px-4 sm:px-6 lg:px-8 mx-auto flex gap-x-2 sm:gap-x-4">
    <svg class="flex-shrink-0 w-[2.375rem] h-[2.375rem] rounded-full" width="38" height="38" viewBox="0 0 38 38" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="38" height="38" rx="6" fill="#2563EB"/>
        <path d="M10 28V18.64C10 13.8683 14.0294 10 19 10C23.9706 10 28 13.8683 28 18.64C28 23.4117 23.9706 27.28 19 27.28H18.25" stroke="white" stroke-width="1.5"/>
        <path d="M13 28V18.7552C13 15.5104 15.6863 12.88 19 12.88C22.3137 12.88 25 15.5104 25 18.7552C25 22 22.3137 24.6304 19 24.6304H18.25" stroke="white" stroke-width="1.5"/>
        <ellipse cx="19" cy="18.6554" rx="3.75" ry="3.6" fill="white"/>
    </svg>
    
    <div class="space-y-3">
        <h2 class="font-medium text-gray-800 dark:text-white">
            {#if apiStatus.data.type === 'sql'}
                <p class="text-gray-800 dark:text-white">
                    {apiStatus.data.text}
                </p>
            {:else}
                <p>我不知道如何处理类型为 {apiStatus.data.type} 的数据</p>
            {/if}
        </h2>
    </div>
</li> 
{:else if apiStatus.status === 'Error'}
  <p>发生错误: {apiStatus.error}</p>
{/if}
