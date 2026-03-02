export type ApiData<T> = 
    | { status: 'NotRequested' }
    | { status: 'Loading' }
    | { status: 'Loaded', data: T }
    | { status: 'Error', error: string }
    ;

export type Page =
    | "training-data"
    | "chat"

// 在MessageContents类型中添加not_logged_in类型
export type MessageContents =
    | { type: 'user_question', question: string }
    | { type: 'question_list', questions: string[], header: string, selected: string | null }
    | { type: 'sql', text: string, id: string }
    | { type: 'df', df: string, id: string }
    | { type: 'plotly_figure', fig: string, id: string }
    | { type: 'error', error: string }
    | { type: 'question_cache', id: string, question: string, sql: string, df: string, fig: string, followup_questions: string[] }
    | { type: 'question_history', questions: QuestionLink[] }
    | { type: 'user_sql' }
    | { type: 'not_logged_in', html: string } // 添加这一行

export type Method =
    | 'GET'
    | 'POST'

export interface QuestionLink {
    question: string,
    id: string
}