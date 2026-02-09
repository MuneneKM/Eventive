import { Navigate, useLocation, Outlet } from 'react-router';
import { useEffect } from 'react';
import { DesktopNav } from '../components/DesktopNav';
import { MobileNav } from '../components/MobileNav';
import { Toaster } from 'sonner';
import { useAuth } from '../context/AuthContext';

export function ProtectedRootLayout() {
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

    // Set currentEventId in localStorage when navigating to an event
    useEffect(() => {
        const parts = location.pathname.split('/');
        const eventIndex = parts.indexOf('event');
        if (eventIndex !== -1 && parts[eventIndex + 1]) {
            localStorage.setItem('currentEventId', parts[eventIndex + 1]);
        }
    }, [location.pathname]);

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
            <DesktopNav />
            <main className="min-h-screen">
                <Outlet />
            </main>
            <MobileNav />
            <Toaster />
        </div>
    );
}
