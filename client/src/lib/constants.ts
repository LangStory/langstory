const BASE_URL: string = process.env.NODE_ENV === 'production' ? 'https://api.langstory.org' : 'http://api.langstory.localhost'
const V1 = `${BASE_URL}/v1`
export const URLS = {
    BASE: BASE_URL,
    REFRESH_TOKEN: (): string => `${BASE_URL}/auth/token/refresh`,
    LOGIN: (): string => `${BASE_URL}/auth/username-password/login`,
    MAGIC_LINK_LOGIN: (id: string, slug: string): string => `${BASE_URL}/login/magic-link/${id}/${slug}`,
    REQUEST_MAGIC_LINK: (): string => `${BASE_URL}/login/magic-link`,
    ORGANIZATIONS: (): string => `${V1}/organizations`,
    LIST_PROJECTS: (): string => `${V1}/projects`,
    GET_PROJECTS: (perPage: number = 1000): string => `${V1}/projects?perPage=${perPage}`,
    GET_PROJECT: (id: string, perPage: number = 1000): string => `${V1}/projects/${id}?perPage=${perPage}`,
    GET_PROJECT_TOOLS: (id: string, perPage: number = 1000): string => `${V1}/projects/${id}/tools?perPage=${perPage}`,
    GET_CHATS: (perPage: number = 1000): string => `${V1}/chats?perPage=${perPage}`,
    GET_CHAT: (id: string): string => `${V1}/chats/${id}`,
    GET_TOOL: (id: string): string => `${V1}/tools/${id}?`,
    CREATE_NEW_CHAT: (): string => `${V1}/chats`,
    CREATE_NEW_MESSAGE: (id: string): string => `${V1}/chats/${id}/messages`,
    GET_CHAT_MESSAGES: (id: string, perPage: number = 1000): string => `${V1}/chats/${id}/messages?perPage=${perPage}`,
}
