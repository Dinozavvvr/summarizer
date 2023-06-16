import "./pages/normalize.css"
import "./pages/vars.css"
import React from 'react';
import {Route, BrowserRouter, Routes} from 'react-router-dom';
import HomePage from "./pages/home/HomePage"
import LoginPage from "./pages/login/LoginPage"
import SignUpPage from "./pages/signup/SignUpPage";
import ProfilePage from "./pages/profile/ProfilePage";
import LogoutPage from "./pages/profile/LogoutPage";
import DocumentsPage from "./pages/document/DocumentsPage";


function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route>
                    <Route index element={<HomePage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/signup" element={<SignUpPage />} />
                    <Route path="/profile" element={<ProfilePage />} />
                    <Route path="/logout" element={<LogoutPage/>} />
                    <Route path="/document" element={<DocumentsPage/>} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
