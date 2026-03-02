<script lang="ts">
    export let onDismiss: () => void;
    export let onTrain: (trainingData: string, trainingDataType: string) => void;
    export let selectedTrainingDataType: string = "SQL";

    interface TrainingOption {
        name: string;
        description: string;
        example: string;
    }

    let options = [
        {
            "name": "DDL",
            "description": "这是定义数据库结构的CREATE TABLE语句。",
            "example": "CREATE TABLE table_name (column_1 datatype, column_2 datatype, column_3 datatype);"
        },
        {
            "name": "文档",
            "description": "可以是任何基于文本的文档。保持内容简短并聚焦于单一主题。",
            "example": "我们对ABC的定义是XYZ。"
        },
        {
            "name": "SQL",
            "description": "可以是任何有效的SQL语句。越多越好。",
            "example": "SELECT column_1, column_2 FROM table_name;"
        }
    ];

    let currentTrainingData: string = "";

    const handleSubmit = () => {
        onTrain(currentTrainingData, selectedTrainingDataType.toLowerCase());
    }
</script>

<!-- 注释表单 -->
<div class="max-w-[85rem] px-4 py-10 sm:px-6 lg:px-8 lg:py-14 mx-auto">
    <div class="mx-auto max-w-2xl">  
      <!-- 卡片 -->
      <div class="mt-5 p-4 relative z-10 bg-white border rounded-xl sm:mt-10 md:p-10 dark:bg-gray-800 dark:border-gray-700">
        <div class="flex justify-between items-center py-3 px-4 border-b dark:border-gray-700 mb-2">
            <h2 class="text-xl text-gray-800 font-bold sm:text-3xl dark:text-white">
              添加训练数据              
            </h2>
            <button on:click={onDismiss} type="button" class="hs-dropdown-toggle inline-flex flex-shrink-0 justify-center items-center h-8 w-8 rounded-md text-gray-500 hover:text-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 focus:ring-offset-white transition-all text-sm dark:focus:ring-gray-700 dark:focus:ring-offset-gray-800" data-hs-overlay="#hs-vertically-centered-modal"><span class="sr-only">关闭</span> <svg class="w-3.5 h-3.5" width="8" height="8" viewBox="0 0 8 8" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0.258206 1.00652C0.351976 0.912791 0.479126 0.860131 0.611706 0.860131C0.744296 0.860131 0.871447 0.912791 0.965207 1.00652L3.61171 3.65302L6.25822 1.00652C6.30432 0.958771 6.35952 0.920671 6.42052 0.894471C6.48152 0.868271 6.54712 0.854471 6.61352 0.853901C6.67992 0.853321 6.74572 0.865971 6.80722 0.891111C6.86862 0.916251 6.92442 0.953381 6.97142 1.00032C7.01832 1.04727 7.05552 1.1031 7.08062 1.16454C7.10572 1.22599 7.11842 1.29183 7.11782 1.35822C7.11722 1.42461 7.10342 1.49022 7.07722 1.55122C7.05102 1.61222 7.01292 1.6674 6.96522 1.71352L4.31871 4.36002L6.96522 7.00648C7.05632 7.10078 7.10672 7.22708 7.10552 7.35818C7.10442 7.48928 7.05182 7.61468 6.95912 7.70738C6.86642 7.80018 6.74102 7.85268 6.60992 7.85388C6.47882 7.85498 6.35252 7.80458 6.25822 7.71348L3.61171 5.06702L0.965207 7.71348C0.870907 7.80458 0.744606 7.85498 0.613506 7.85388C0.482406 7.85268 0.357007 7.80018 0.264297 7.70738C0.171597 7.61468 0.119017 7.48928 0.117877 7.35818C0.116737 7.22708 0.167126 7.10078 0.258206 7.00648L2.90471 4.36002L0.258206 1.71352C0.164476 1.61976 0.111816 1.4926 0.111816 1.36002C0.111816 1.22744 0.164476 1.10028 0.258206 1.00652Z" fill="currentColor"></path></svg></button>
        </div>
    
            <span class="block mb-2 text-sm font-medium dark:text-white">训练数据类型</span>
            <div class="grid space-y-3 mb-1">
                {#each options as {name, description, example}}
                    <div class="relative flex items-start">
                        <div class="flex items-center h-5 mt-1">
                        <input id="hs-radio-{name}" bind:group={selectedTrainingDataType} value={name} name="hs-radio-with-description" type="radio" class="border-gray-200 rounded-full text-blue-600 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700 dark:checked:bg-blue-500 dark:checked:border-blue-500 dark:focus:ring-offset-gray-800" aria-describedby="hs-radio-delete-description">
                        </div>
                        <label for="hs-radio-{name}" class="ml-3">
                        <span class="block text-sm font-semibold text-gray-800 dark:text-gray-300">{name}</span>
                        <span id="hs-radio-ddl-description" class="block text-sm text-gray-600 dark:text-gray-500">{description}</span>
                        </label>
                    </div>
                {/each}  
            </div>

          <div class="mt-2 border-t dark:border-gray-700">
            <label for="hs-feedback-post-comment-textarea-1" class="block mt-2 mb-2 text-sm font-medium dark:text-white">您的{selectedTrainingDataType}</label>
            <div class="mt-1">
              <textarea bind:value={currentTrainingData} id="hs-feedback-post-comment-textarea-1" name="hs-feedback-post-comment-textarea-1" rows="3" class="py-3 px-4 block w-full border border-gray-200 rounded-md text-sm focus:border-blue-500 focus:ring-blue-500 sm:p-4 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400" placeholder="{options.find(option => option.name === selectedTrainingDataType)?.example ?? '无示例可用'}"></textarea>
            </div>
          </div>
  
          <div class="mt-6 grid">
            <button on:click={handleSubmit} class="py-3 px-4 inline-flex justify-center items-center gap-2 rounded-md border border-transparent font-semibold bg-blue-500 text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all dark:focus:ring-offset-gray-800">保存</button>
          </div>
      </div>
      <!-- 结束卡片 -->
    </div>
  </div>
  <!-- 结束注释表单 -->