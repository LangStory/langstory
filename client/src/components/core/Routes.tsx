import { RollbarContext } from '@rollbar/react'
import { ReactNode } from 'react'
import { Route, Routes, Navigate } from 'react-router-dom'
import { useAuth } from 'hooks/use-auth'
import AuthRoute from 'components/core/AuthRoute'
import NoAuthRoute from 'components/core/NoAuthRoute'
import Navbar from 'components/core/Navbar'

import Login from 'pages/Login'
import MagicLinkLogin from 'pages/MagicLinkLogin.tsx'
import Settings from 'pages/Settings.tsx'
import ChatsList from 'pages/ChatsList.tsx'
import Chat from 'pages/Chat.tsx'

function withNoAuth(children: ReactNode): ReactNode {
    return (
        <NoAuthRoute>
            {children}
        </NoAuthRoute>
    )
}

function withAuth(children: ReactNode): ReactNode {
    return (
        <AuthRoute>
            {children}
        </AuthRoute>
    )
}

function withNavbar(children: ReactNode): ReactNode {
    return (
        <Navbar>
            {children}
        </Navbar>
    )
}

function withRollbarContext(name: string, children: ReactNode): ReactNode {
    return (
        <RollbarContext context={name}>
            {children}
        </RollbarContext>
    )
}

function withAuthNavbarRollbar(name: string, children: ReactNode): ReactNode {
    return (
        <AuthRoute>
            <Navbar>
                <RollbarContext context={name}>
                    {children}
                </RollbarContext>
            </Navbar>
        </AuthRoute>
    )
}

// ==========================================
// ROUTES
// ==========================================
export default function AppRoutes() {
    const {user} = useAuth()
    const navigateToDefault = () => user ? <Navigate to={'/home'}/> : <Navigate to="/login"/>

    return (
        <Routes>
            {/*------- PRIVATE ROUTES -------*/}
            <Route path="/chats">
                <Route index element={withNoAuth(withNavbar(<ChatsList/>))}/>
                <Route path=":id" element={withNoAuth(withNavbar(<Chat/>))}/>
                {/*<Route index element={withAuthNavbarRollbar('receiving-tasks', <ChatsList/>)}/>*/}
                {/*<Route path=":id" element={withAuthNavbarRollbar('receiving-task/details', <Chat/>)}/>*/}

            </Route>
            <Route path="/settings" element={withAuthNavbarRollbar('settings', <Settings/>)}/>


            {/*------- PUBLIC ROUTES -------*/}
            <Route path="login" element={withNoAuth(withRollbarContext('login', <Login/>))}/>
            <Route path="magic-link" element={withNoAuth(withRollbarContext('magic-link-login', <MagicLinkLogin/>))}/>


            {/*REDIRECT FROM AN AUTH ROUTE OR GOING TO '/' */}
            <Route index element={navigateToDefault()}/>

            {/*REDIRECT WHEN ROUTE IS NOT FOUND */}
            <Route path="*" element={navigateToDefault()}/>
        </Routes>
    )
}
