import { ReactNode } from 'react'
import { Route, Routes, Navigate } from 'react-router-dom'
import AuthRoute from './AuthRoute'
import NoAuthRoute from './NoAuthRoute'
import { useAuth } from '../../hooks/use-auth'
import Navbar from './Navbar'

import QrReader from '../QrScanner.tsx'
import Login from '../../pages/Login'
import ReceivingTasks from '../../pages/ReceivingTasks.tsx'
import ReceivingTaskDetail from '../../pages/ReceivingTaskDetail.tsx'
import PickingJob from '../../pages/PickingJob.tsx'
import AddReceivingTaskItem from '../../pages/AddReceivingTaskItem.tsx'
import ReceivingTaskItemDetail from '../../pages/ReceivingTaskItemDetail.tsx'
import MagicLinkLogin from '../../pages/MagicLinkLogin.tsx'
import Settings from '../../pages/Settings.tsx'
import { RollbarContext } from '@rollbar/react'

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
    const navigateToDefault = () => user ? <Navigate to={'/receiving-tasks'}/> : <Navigate to="/login"/>

    return (
        <Routes>
            {/*------- PRIVATE ROUTES -------*/}
            <Route path="/receiving-task-item">
                <Route path=":id" element={withAuthNavbarRollbar('receiving-task-item/details', <ReceivingTaskItemDetail/>)}/>
            </Route>
            <Route path="/receiving-tasks">
                <Route index element={withAuthNavbarRollbar('receiving-tasks', <ReceivingTasks/>)}/>
                <Route path=":id" element={withAuthNavbarRollbar('receiving-task/details', <ReceivingTaskDetail/>)}/>
                <Route path=":id/add-item" element={withAuthNavbarRollbar('receiving-task/details/add-item', <AddReceivingTaskItem/>)}/>
            </Route>
            <Route path="/settings" element={withAuthNavbarRollbar('settings', <Settings/>)}/>
            <Route path="/picking-job" element={withAuthNavbarRollbar('picking-job', <PickingJob/>)}/>
            <Route path="/qr-reader" element={withAuthNavbarRollbar('qr-reader', <QrReader/>)}/>


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
