const BASE_URL: string = process.env.NODE_ENV === 'production' ? 'https://api.langstory.org' : 'http://api.langstory.localhost'
const V1 = `${BASE_URL}/v1`
export const URLS = {
    BASE: BASE_URL,
    REFRESH_TOKEN: (): string => `${BASE_URL}/auth/token/refresh`,
    LOGIN: (): string => `${BASE_URL}/auth/username-password/login`,
    MAGIC_LINK_LOGIN: (id: string, slug: string): string => `${BASE_URL}/login/magic-link/${id}/${slug}`,
    REQUEST_MAGIC_LINK: (): string => `${BASE_URL}/login/magic-link`,
    ORGANIZATIONS: (): string => `${V1}/organizations`,
    GET_CHAT: (id: string): string => `${V1}/chats/${id}`,
    CREATE_NEW_CHAT: (): string => `${V1}/chats`,
}
