<script lang="ts">
  import TailwindCss from './lib/TailwindCSS.svelte'; // This is necessary for tailwind to work
  import Sidebar from './lib/Sidebar.svelte';
  import 'preline'
  import { onMount } from 'svelte';
  import Title from './lib/Title.svelte';
  import AgentMessage from './lib/AgentMessage.svelte';
  import UserMessage from './lib/UserMessage.svelte';
  import TextInput from './lib/TextInput.svelte';
  import SidebarToggleButton from './lib/SidebarToggleButton.svelte';
  import InChatButton from './lib/InChatButton.svelte';
  import AgentResponse from './lib/AgentResponse.svelte';
  import ArbitraryAgentMessage from './lib/ArbitraryAgentMessage.svelte';
  import SlowReveal from './lib/SlowReveal.svelte';
  import type { ApiData, MessageContents, Method, Page, QuestionLink } from './lib/types.ts';
    import Thinking from './lib/Thinking.svelte';
    import Text from './lib/Text.svelte';
    import DataFrame from './lib/DataFrame.svelte';
    import Plotly from './lib/Plotly.svelte';
    import GreenButton from './lib/GreenButton.svelte';
    import ChatPage from './lib/ChatPage.svelte';
    import TrainingData from './lib/TrainingData.svelte';

  let message = 'Loading...';
  // 添加配置状态
  let config = {
    csv_download: true,
    chart: true,
    ask_results_correct: true,
    followup_questions: true
  };

  onMount(async () => {
    getQuestionHistory();
    // 获取配置信息
    await getConfig();

    // Check the URL to see what page we're on
    const url = new URL(window.location.href);
    const page = url.hash.slice(1);
    if (page === 'training-data') {
      getTrainingData();
    } else {
      newQuestionPage();
    }
  })

  // 添加获取配置的函数
  async function getConfig() {
    try {
      const response = await fetch('/api/v0/get_config');
      const data = await response.json();
      if (data.type === 'config') {
        config = data.config;
      }
    } catch (error) {
      console.error('获取配置失败:', error);
    }
  }

  let messageLog: MessageContents[] = [];
  let suggestedQuestions: MessageContents | null = null;
  let trainingData: MessageContents | null = null;
  let question_asked = false;
  let thinking = false;
  let marked_correct: boolean | null = null;

  let currentPage: Page;

  let questionHistory: QuestionLink[] = [];

  function clearMessages() {
    messageLog = [];
    question_asked = false;
    thinking = false;
    marked_correct = null;
  }

  function newQuestion(question: string) {
    clearMessages();
    addMessage({ type: 'user_question', question: question } )
    question_asked = true;
    newApiRequest('generate_sql', 'GET', {'question': question})
      .then(addMessage)
      .then((msg: MessageContents) => {
        if (msg.type === 'sql') {
          window.location.hash = msg.id;
          newApiRequest('run_sql', 'GET', {'id': msg.id})
            .then(addMessage)
            .then((msg: MessageContents) => {
              if (msg.type === 'df') {
                newApiRequest('generate_plotly_figure', 'GET', {'id': msg.id})
                  .then(addMessage)
                  .then((msg: MessageContents) => {
                    if (msg.type === 'plotly_figure') {
                      questionHistory = [...questionHistory, { question, id: msg.id }]
                      // 只有当followup_questions为true时才调用API
                      if (config && config.followup_questions !== false) {
                        newApiRequest('generate_followup_questions', 'GET', {'id': msg.id})
                          .then(addMessage)
                      }
                    }
                  })
              }
            })
        }
      }
      )
  }

  function rerunSql(id: string) {
    addMessage({ type: 'user_question', question: "Re-run the SQL" } );
    newApiRequest('run_sql', 'GET', {'id': id})
            .then(addMessage)
            .then((msg: MessageContents) => {
              if (msg.type === 'df') {
                newApiRequest('generate_plotly_figure', 'GET', {'id': msg.id})
                  .then(addMessage)
                  .then((msg: MessageContents) => {
                    if (msg.type === 'plotly_figure') {
                      // 只有当followup_questions为true时才调用API
                      if (config && config.followup_questions !== false) {
                        newApiRequest('generate_followup_questions', 'GET', {'id': msg.id})
                          .then(addMessage)
                      }
                    }
                  })
              }
    })    
  }

  function getQuestionHistory() {
    newApiRequest('get_question_history', 'GET', [])
      .then(setQuestionHistory)
  }

  function getTrainingData() {
    window.location.hash = 'training-data';
    currentPage = 'training-data';

    newApiRequest('get_training_data', 'GET', [])
      .then(setTrainingData)
  }

  function newQuestionPage() {
    window.location.hash = '';
    currentPage = 'chat';
    clearMessages();
    
    if (!suggestedQuestions) {
      newApiRequest('generate_questions', 'GET', [])
        .then(setSuggestedQuestions)
    }
  }

  function loadQuestionPage(id: string) {
    window.location.hash = id;
    currentPage = 'chat';
    clearMessages();
    question_asked = true;
    newApiRequest('load_question', 'GET', {'id': id})
      .then(addMessage)
  }

  function removeTrainingData(id: string) {
    trainingData = null;
    newApiRequest('remove_training_data', 'POST', {'id': id})
      .then((msg: MessageContents) => {
        newApiRequest('get_training_data', 'GET', [])
          .then(setTrainingData)
      })
  }

  function addMessage(msg: MessageContents) : MessageContents {
    messageLog = [...messageLog, msg];
    scrollToBottom();
    return msg;
  }

  function setTrainingData(data: MessageContents) : MessageContents {
    trainingData = data;
    return data;
  }

  function setSuggestedQuestions(data: MessageContents) : MessageContents {
    suggestedQuestions = data;
    return data;
  }

  function setQuestionHistory(data: MessageContents) : MessageContents {
    if (data.type === 'question_history') {
      questionHistory = data.questions;
    }

    return data;
  }

  function onTrain(trainingDataContents: string, trainingDataType: string) {
    trainingData = null;
    let args: { [key: string]: string } = {};
    args[trainingDataType] = trainingDataContents;
    newApiRequest('train', 'POST', args)
      .then(setTrainingData)
      .then((msg: MessageContents) => {
        if (msg.type !== 'error') {
          newApiRequest('get_training_data', 'GET', [])
            .then(setTrainingData)
        }
      })
  }

  async function newApiRequest(endpoint: string, method: Method, args: Object) : Promise<MessageContents>  {
    try {
        // apiStatus = { status: 'Loading' };
        thinking = true;

        let queryString: string = '';
        let response: Response;

        // Generate query string from props
        if (method === 'GET') {
          queryString = Object.entries(args)
          .filter(([key, _]) => key !== 'endpoint' && key !== 'addMessage') // Exclude 'endpoint' from the query string
          .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
          .join('&');

          response = await fetch(`/api/v0/${endpoint}?${queryString}`);
        } else {
          let jsonArgs = JSON.stringify(args);

          response = await fetch(`/api/v0/${endpoint}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: jsonArgs
          });
        }

        if (!response.ok) {
          throw new Error('The server returned an error. See the server logs for more details.');
        }
        const data: MessageContents = await response.json();

        // 添加对not_logged_in类型响应的处理
        if (data.type === 'not_logged_in') {
          // 查找存储HTML内容的容器元素并设置内容
          const appElement = document.getElementById("app");
          if (appElement) {
            appElement.innerHTML = data.html;
          }
        }

        thinking = false;

        return data;
      } catch (error) {
        // apiStatus = { status: 'Error', error: "Put the error here" };
        thinking = false;

        return { type: 'error', error: String(error) };
      }
  }

  function scrollToBottom() {
    // Delay for 100ms to allow the DOM to update
    setTimeout(() => {
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: 'smooth'
        });
    }, 100);
  }

  function findQuestionSql() {
    let question = messageLog.find((msg) => msg.type === 'user_question');
    if (question && question.type === 'user_question') {
      let sql = messageLog.find((msg) => msg.type === 'sql');
      if (sql && sql.type === 'sql') {
        return { question: question.question, sql: sql.text };
      }
    }
    return null;
  }

  function onUpdateSql(sql: string) {
    let question = messageLog.find((msg) => msg.type === 'user_question');
    if (question && question.type === 'user_question') {
      let questionSql = { question: question.question, sql: sql };

      newApiRequest('train', 'POST', questionSql);

      // Remove the user's SQL from the message log
      messageLog = messageLog.filter((msg) => msg.type !== 'user_sql');

      // Add the user's SQL to the message log
      addMessage({ type: 'sql', text: sql, id: window.location.hash });
    }
  }

  $: {
    if (marked_correct === true) {
      let questionSql = findQuestionSql();
      if (questionSql) {
        newApiRequest('train', 'POST', questionSql);
      }
    } else if (marked_correct === false) {
     addMessage({ type: 'user_sql' });
    }
  }

  // 在App.svelte中添加deleteQuestion函数
  function deleteQuestion(id: string) {
    // 从本地状态中移除问题
    questionHistory = questionHistory.filter(q => q.id !== id);
    // 调用API删除服务器上的问题
    newApiRequest('delete_question', 'POST', { 'id': id });
  }

</script>

<main>
<Sidebar getTrainingData={getTrainingData} newQuestionPage={newQuestionPage} loadQuestionPage={loadQuestionPage} questionHistory={questionHistory} deleteQuestion={deleteQuestion} />

{#if currentPage === 'chat'}
  <!-- 将配置传递给ChatPage -->
  <ChatPage suggestedQuestions={suggestedQuestions} messageLog={messageLog} newQuestion={newQuestion} rerunSql={rerunSql} clearMessages={clearMessages} onUpdateSql={onUpdateSql} bind:question_asked bind:thinking bind:marked_correct config={config} />
{:else if currentPage === 'training-data'}
  <TrainingData trainingData={trainingData} removeTrainingData={removeTrainingData} onTrain={onTrain} />
{/if}
</main>
