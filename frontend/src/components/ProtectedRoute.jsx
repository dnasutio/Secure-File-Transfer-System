import {Navigate} from 'react-router-dom'
import {jwtDecode} from 'jwt-decode'
import api from '../api'
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../constants'
import { useState, useEffect } from 'react'

function ProtectedRoute({ children }) {
    const [isAuthorized, setIsAuthorized] = useState(null);

    // As soon as ProtectedRoute is loaded, do auth and if something goes wrong set authorized to false
    useEffect(() => {
        auth().catch(() => setIsAuthorized(false))
    }, []);

    // Handles requests to refresh access token
    const refreshToken = async () => {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN)
        try {
            // Make a request to backend api using refresh token
            const res = await api.post("/api/token/refresh/", {
                refresh: refreshToken,
            });
            if (res.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, res.data.access)
                setIsAuthorized(true)
            } else {
                setIsAuthorized(false)
            }
        } catch (error) {
            console.log(error);
            setIsAuthorized(false);
        }
    }

    // Handles verifying the existance of the access token in local storage
    const auth = async () => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (!token) {
            setIsAuthorized(false);
            return
        }

        // Decode the token to get the expiration date
        const decoded = jwtDecode(token);
        const tokenExpiration = decoded.exp;
        const now = Date.now() / 1000;

        // If current access token is expired get a new token using refresh token
        if (tokenExpiration < now) {
            await refreshToken();
        } else {
            setIsAuthorized(true);
        }
    }

    // Load until auth process finished
    if (isAuthorized === null) {
        return <div>Loading...</div>
    }

    // If authorized proceed to protected route else go back to log in page
    return isAuthorized ? children : <Navigate to="login" />
}

export default ProtectedRoute