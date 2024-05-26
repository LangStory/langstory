import * as jwt from 'jwt-decode'

    export interface User {
        id: string;
        first_name: string;
        last_name: string;
        email_address: string;
        avatar_url?: string;
        organizations?: [string];
    }

    export interface Organization {
        id: string;
        name: string;
        logo_url?: string;
    }

    export interface AuthJwtPayload extends jwt.JwtPayload {
        user: User;
        org?: Organization;
    }

    // for verbosity, no real function
    export interface RefreshJwtPayload extends jwt.JwtPayload {
    }
