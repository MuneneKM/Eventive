import { Navigate, useLocation, Outlet } from 'react-router';
import { useAuth } from '../context/AuthContext';

// Wrapper for protected routes (require authentication)
export function ProtectedLayout() {
    const { isAuthenticated, isLoading } = useAuth();
    const location = useLocation();

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    if (!isAuthenticated) {
        // Redirect to login while saving the current location
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    return (
        <>
            <Outlet />
        </>
    );
}

// Wrapper for public routes (redirect to dashboard if authenticated)
export function PublicLayout() {
    const { isAuthenticated, isLoading } = useAuth();
    const location = useLocation();

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    // If authenticated and trying to access login/register, redirect to dashboard
    if (isAuthenticated && (location.pathname === '/login' || location.pathname === '/register')) {
        return <Navigate to="/dashboard" state={{ from: location }} replace />;
    }

    return (
        <>
            <Outlet />
        </>
    );
}
