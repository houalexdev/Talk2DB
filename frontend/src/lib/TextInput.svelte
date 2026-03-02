<script lang="ts">
    export let onSubmit: (message: string) => void; // a callback function that will be called on Submit
    let newMessage = '';
  
    function handleKeydown(event: KeyboardEvent) {
        if (event.key === "Enter") {
        onSubmit(newMessage);
        event.preventDefault(); // prevent any default action
        }
    }

    function handleClick() {
        onSubmit(newMessage);
    }
  </script>

    <!-- Input -->
    <div class="relative">
        <input type="text" bind:value={newMessage} on:keydown={handleKeydown} class="p-4 pb-12 block w-full bg-gray-100 border-gray-200 rounded-md text-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-slate-800 dark:border-gray-700 dark:text-gray-400" placeholder="请向我提问有关您数据的问题，我可以将其转换为SQL查询。">
  
        <!-- Toolbar -->
        <div class="absolute bottom-px inset-x-px p-2 rounded-b-md bg-gray-100 dark:bg-slate-800">
          <div class="flex justify-between items-center">
            <!-- Button Group -->
            <div class="flex items-center">

            </div>
            <!-- End Button Group -->
  
            <!-- Button Group -->
            <div class="flex items-center gap-x-1">
              <!-- Send Button -->
              <button type="button" on:click={handleClick} class="inline-flex flex-shrink-0 justify-center items-center h-8 w-8 rounded-md text-white bg-blue-600 hover:bg-blue-500 focus:z-10 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all">
                <svg class="h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                  <path d="M15.964.686a.5.5 0 0 0-.65-.65L.767 5.855H.766l-.452.18a.5.5 0 0 0-.082.887l.41.26.001.002 4.995 3.178 3.178 4.995.002.002.26.41a.5.5 0 0 0 .886-.083l6-15Zm-1.833 1.89L6.637 10.07l-.215-.338a.5.5 0 0 0-.154-.154l-.338-.215 7.494-7.494 1.178-.471-.47 1.178Z"/>
                </svg>
              </button>
              <!-- End Send Button -->
            </div>
            <!-- End Button Group -->
          </div>
        </div>
        <!-- End Toolbar -->
      </div>
      <!-- End Input -->