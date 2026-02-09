import { useNavigate } from 'react-router';
import { Home, ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui/button';

export function NotFound() {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex items-center justify-center px-4">
            <div className="text-center">
                <div className="mb-8">
                    <h1 className="text-9xl font-bold text-blue-600">404</h1>
                </div>
                <h2 className="text-3xl font-semibold mb-4">Page Not Found</h2>
                <p className="text-gray-600 dark:text-gray-300 mb-8 max-w-md mx-auto">
                    Sorry, the page you're looking for doesn't exist or has been moved.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <Button
                        size="lg"
                        onClick={() => navigate(-1)}
                        variant="outline"
                        className="flex items-center gap-2"
                    >
                        <ArrowLeft className="size-5" />
                        Go Back
                    </Button>
                    <Button
                        size="lg"
                        onClick={() => navigate('/')}
                        className="flex items-center gap-2"
                    >
                        <Home className="size-5" />
                        Go Home
                    </Button>
                </div>
            </div>
        </div>
    );
}
