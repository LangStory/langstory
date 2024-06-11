interface ResponseTokenUser {
    email_address: string
    first_name: string
    last_name: string
    avatar_url?: string
    organizations?: [string]
    id: string
}

interface ResponseTokenOrganization {
    id: string
    name: string
    logo_url?: string
}

interface ResponseTokenData {
    user: ResponseTokenUser
    org?: ResponseTokenOrganization

}

export default interface RefreshTokenResponse {
    token: string
    data?: ResponseTokenData
}

