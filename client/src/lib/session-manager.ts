const KEY_PREFIX = '__LANGSTORY__'

export const STORAGE_KEYS = {
    ACCESS_TOKEN: `${KEY_PREFIX}access-token`,
    REFRESH_TOKEN: `${KEY_PREFIX}refresh-token`,
}

export function deleteValue(key: string) {
    window.localStorage.removeItem(`${KEY_PREFIX}${key}`)
}

export function storeValue(key: string, val: any) {
    if (typeof val === 'string' || (val instanceof String)) window.localStorage.setItem(`${KEY_PREFIX}${key}`, val as string)
    else window.localStorage.setItem(`${KEY_PREFIX}${key}`, JSON.stringify(val))
}

export function getValue(key: string): string {
    return window.localStorage.getItem(`${KEY_PREFIX}${key}`) || ''
}
