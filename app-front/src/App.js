import "./pages/normalize.css"
import "./pages/vars.css"
import React, {useEffect, useState} from 'react';
import {Route, BrowserRouter, Routes, useNavigate, Navigate, Outlet} from 'react-router-dom';
import HomePage from "./pages/home/HomePage"
import LoginPage from "./pages/login/LoginPage"
import SignUpPage from "./pages/signup/SignUpPage";
import ProfilePage from "./pages/profile/ProfilePage";
import LogoutPage from "./pages/profile/LogoutPage";
import DocumentsPage from "./pages/document/DocumentsPage";
import DocumentCreatePage from "./pages/document/DocumentCreatePage";
import DocumentPage from "./pages/document/DocumentPage";
import CollectionsPage from "./pages/collection/CollectionsPage";
import CollectionEditPage from "./pages/collection/CollectionEditPage";
import CollectionPage from "./pages/collection/CollectionPage";
import CollectionAddDocumentsPage from "./pages/collection/CollectionAddDocumentsPage";
import CollectionTraineePage from "./pages/collection/CollectionTraineePage";
import CollectionSummarizePage from "./pages/collection/CollectionSummarizePage";
import {HOST} from "./config/config";
import Header from "./components/header/Header";
import {getMenuItems} from "./utils";

const ProtectedRoute = ({user, redirectPath = '/', children,}) => {
    console.log(user)
    if (!user) {
        return <Navigate to={redirectPath} replace />;
    }

    return children ? children : <Outlet/>;
};

function App() {

    const [user, setUser] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const token = localStorage.getItem('accessToken');

    const getUser = async () => {
        if (!token) {
            setIsLoading(false);
            return;
        }

        try {
            const response = await fetch(`http://${HOST}/user/me/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ' + token,
                },
            });

            if (response.ok) {
                const data = await response.json();
                setUser(data);
            }
        } catch (error) {
            console.error('An error occurred:', error);
        }

        setIsLoading(false);
    };

    useEffect(() => {
        getUser();
    }, [token]);

    if (isLoading) {
        return <></>;
    }
    return (
        <BrowserRouter>
            <Routes>
                <Route>
                    <Route index element={<HomePage/>}/>
                    <Route path="/login" element={<LoginPage/>}/>
                    <Route path="/signup" element={<SignUpPage/>}/>
                    <Route path="/logout" element={<LogoutPage/>}/>
                    <Route element={<ProtectedRoute user={user}/>}>
                        <Route path="/profile" element={<ProfilePage/>}/>
                        <Route path="/document" element={<DocumentsPage/>}/>
                        <Route path="/document/create" element={<DocumentCreatePage/>}/>
                        <Route path="/document/:id" element={<DocumentPage/>}/>
                        <Route path="/collection" element={<CollectionsPage/>}/>
                        <Route path="/collection/create" element={<CollectionEditPage/>}/>
                        <Route path="/collection/edit/:id" element={<CollectionEditPage/>}/>
                        <Route path="/collection/:id/documents" element={<CollectionAddDocumentsPage/>}/>
                        <Route path="/collection/:id/trainee" element={<CollectionTraineePage/>}/>
                        <Route path="/collection/:id/summarize" element={<CollectionSummarizePage/>}/>
                        <Route path="/collection/:id" element={<CollectionPage/>}/>
                    </Route>
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
