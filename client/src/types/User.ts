export interface User {
    id: string;
    first_name: string;
    last_name: string;
    email_address: string;
    avatar_url?: string;
    organizations?: [string];
}
