import { JwtPayload } from 'jwt-decode'
import { User } from './User.ts'
import { Organization } from './Organization.ts'

export interface AuthJwtPayload extends JwtPayload {
    user: User;
    org?: Organization;
}
