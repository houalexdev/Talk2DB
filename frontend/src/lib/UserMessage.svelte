<script>
    import Text from "./Text.svelte";

    /** @type {string} */
    export let message;

</script>

<!-- Chat Bubble -->
      <li class="py-2 sm:py-4">
        <div class="max-w-4xl px-4 sm:px-6 lg:px-8 mx-auto">
          <div class="max-w-2xl flex gap-x-2 sm:gap-x-4">
            <span class="flex-shrink-0 inline-flex items-center justify-center h-[2.375rem] w-[2.375rem] rounded-full bg-gray-600">
              <span class="text-sm font-medium text-white leading-none">您</span>
            </span>

            <div class="grow mt-2 space-y-3">
              <Text>
                {message}
              </Text>
              <slot />
            </div>
          </div>
        </div>
      </li>
      <!-- End Chat Bubble -->