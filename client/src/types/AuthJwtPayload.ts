import { JwtPayload } from 'jwt-decode'
import { User } from 'types/User.ts'
import { Organization } from 'types/Organization.ts'

export interface AuthJwtPayload extends JwtPayload {
    user: User;
    org?: Organization;
}
