import {useEffect} from 'react';
import {useNavigate} from 'react-router-dom';

const LogoutPage = () => {
    const navigate = useNavigate();

    useEffect(() => {
        logoutUser();
        navigate('/')

        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const logoutUser = () => {
        localStorage.removeItem('accessToken');
    };
};

export default LogoutPage;
