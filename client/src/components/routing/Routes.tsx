import { RollbarContext } from '@rollbar/react'
import { ReactNode, useEffect, useState } from 'react'
import { Route, Routes, Navigate } from 'react-router-dom'
import { useAuth } from '@hooks/use-auth'
import AuthRoute from '@components/routing/AuthRoute'
import NoAuthRoute from '@components/routing/NoAuthRoute'
import Navbar from '@components/core/Navbar'

import Login from '@pages/Login'
import MagicLinkLogin from '@pages/MagicLinkLogin.tsx'
import Settings from '@pages/Settings.tsx'
import ChatsList from '@pages/ChatsList.tsx'
import ChatComponent from '@pages/ChatComponent.tsx'
import ProjectsList from '@pages/ProjectsList.tsx'
import ProjectComponent from '@pages/ProjectComponent.tsx'
import ProjectToolComponent from '@pages/ProjectToolComponent.tsx'

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
    return withAuth(withNavbar(withRollbarContext(name, children)))
}

// ==========================================
// ROUTES
// ==========================================
export default function AppRoutes() {
    //==============================
    // STATE FOR TRACKING TOKENS
    //==============================
    const {user, signOut, accessTokenExpired, refreshTokenExpired, refreshAccessToken} = useAuth()
    const [isRefreshing, setIsRefreshing] = useState<boolean>(true)
    const navigateToDefault = () => user ? <Navigate to={'/chats'}/> : <Navigate to="/login"/>

    //==============================
    // CHECK JWT TOKENS ARE VALID
    // ONLY CHECK IF USER IS CHANGES
    //==============================
    useEffect(() => {
        const checkTokens = async () => {
            console.log('Checking tokens...')
            if (refreshTokenExpired()) {
                console.log('Refresh token expired. Signing out.')
                signOut()
            } else if (accessTokenExpired()) {
                console.log('Access token expired. Refreshing access token.')
                try {
                    await refreshAccessToken()
                    console.log('Access token refreshed.')
                } catch (error) {
                    console.error('Failed to refresh access token:', error)
                    signOut()
                } finally {
                    setIsRefreshing(false)
                }
            } else {
                console.log('Tokens are valid.')
                setIsRefreshing(false)
            }
        }

        checkTokens().then()
    }, [user])

    //==============================
    // IF LOGGED IN AND TOKEN
    // IS REFRESHING RENDER NOTHING
    //==============================
    if (user && isRefreshing) {
        return <></>
    }

    //==============================
    // RENDER ROUTES
    //==============================
    return (
        <Routes>
            {/*=================================*/}
            {/*PRIVATE ROUTES*/}
            {/*=================================*/}
            <Route path="chats">
                <Route index element={withAuthNavbarRollbar('chats-list', <ChatsList/>)}/>
                <Route path=":id" element={withAuthNavbarRollbar('chat', <ChatComponent/>)}/>
            </Route>

            <Route path="projects">
                <Route index element={withAuthNavbarRollbar('projects-list', <ProjectsList/>)}/>
                <Route path=":id">
                    <Route index element={withAuthNavbarRollbar('project', <ProjectComponent/>)}/>
                    <Route path="tools">
                        <Route path=":id" element={withAuthNavbarRollbar('project-tool', <ProjectToolComponent/>)}/>
                    </Route>
                </Route>
            </Route>

            <Route path="settings" element={withAuthNavbarRollbar('settings', <Settings/>)}/>

            {/*=================================*/}
            {/*PUBLIC ROUTES*/}
            {/*=================================*/}
            <Route path="login" element={withNoAuth(withRollbarContext('login', <Login/>))}/>
            <Route path="magic-link" element={withNoAuth(withRollbarContext('magic-link-login', <MagicLinkLogin/>))}/>

            {/*=================================*/}
            {/*REDIRECT FROM AN AUTH ROUTE OR GOING TO '/' */}
            {/*=================================*/}
            <Route index element={navigateToDefault()}/>

            {/*=================================*/}
            {/*REDIRECT WHEN ROUTE IS NOT FOUND */}
            {/*=================================*/}
            <Route path="*" element={navigateToDefault()}/>
        </Routes>
    )
}
