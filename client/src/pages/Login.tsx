import { FormEvent, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import axios, { AxiosError, AxiosResponse } from 'axios'
import { StatusCodes } from 'http-status-codes'
import { useRollbar } from '@rollbar/react'
import  RefreshTokenResponse  from '../types/Auth.ts'
import { STORAGE_KEYS, storeValue } from '../lib/session-manager.ts'
import { useAuth } from '../hooks/use-auth.tsx'
import { URLS } from '../lib/constants.ts'

function Login() {
    const navigate = useNavigate()
    const rollbar = useRollbar()
    const {updateAuth} = useAuth()
    const [email, setEmail] = useState<string>('')
    const [password, setPassword] = useState<string>('')
    const [error, setError] = useState<string>('')

    async function onSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault()
        if (email === '' || password === '') {
            setError('Please provide an email and password')
        } else {
            const formData = new FormData()
            formData.append('username', email)
            formData.append('password', password)
            try {
                const response: AxiosResponse<RefreshTokenResponse> = await axios.post<RefreshTokenResponse>(URLS.LOGIN(), formData)
                if (response.status === StatusCodes.OK) {
                    const token: string = response.data.token
                    storeValue(STORAGE_KEYS.REFRESH_TOKEN, token)
                    updateAuth()
                    navigate('/chats')
                } else setError('Couldn\'t log in.')
            } catch (e) {
                const error = e as AxiosError
                if (error.request && error.request.status === StatusCodes.UNAUTHORIZED) setError('Incorrect Email or Password')
                else {
                    setError((e as Error).message)
                    rollbar.error(error)
                }
            }
        }
    }

    return (
        <div className="h-screen sm:bg-white md:bg-gray-100 font-droid text-slate-900">

            <div className="flex min-h-full flex-1 flex-col justify-center py-12 sm:px-6 lg:px-8">
                <div className="sm:mx-auto sm:w-full sm:max-w-md">
                    <h2 className="mt-6 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
                        Sign in to your account
                    </h2>
                </div>

                <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-[480px]">
                    <div className="bg-white px-6 py-12 md:shadow sm:rounded-lg sm:px-12">
                        <form className="space-y-6" onSubmit={async (event: FormEvent<HTMLFormElement>) => await onSubmit(event)}>
                            <div>
                                <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
                                    Email address
                                </label>
                                <div className="mt-2">
                                    <input
                                        id="email"
                                        name="email"
                                        type="email"
                                        autoComplete="email"
                                        required
                                        onChange={(e) => setEmail(e.target.value)}
                                        className="px-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm sm:leading-6"
                                    />
                                </div>
                            </div>

                            <div>
                                <label htmlFor="password" className="block text-sm font-medium leading-6 text-gray-900">
                                    Password
                                </label>
                                <div className="mt-2">
                                    <input
                                        id="password"
                                        name="password"
                                        type="password"
                                        autoComplete="current-password"
                                        required
                                        onChange={(e) => setPassword(e.target.value)}
                                        className="px-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm sm:leading-6"
                                    />
                                </div>
                            </div>

                            <div className="flex flex-col items-center">
                                <div className="w-full my-4 text-red-500 text-sm text-center">{error}</div>
                                <div className="w-full text-sm leading-6 text-right">
                                    <Link to="/magic-link " className="font-semibold text-blue-500 hover:text-blue-500">
                                        Sign in with Magic Link
                                    </Link>
                                </div>
                            </div>

                            <div>
                                <button
                                    type="submit"
                                    className="flex w-full justify-center rounded-md bg-blue-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-500"
                                >
                                    Sign in
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Login
