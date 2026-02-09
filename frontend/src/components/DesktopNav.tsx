import { Calendar, FileText, Home, Moon, Network, Sun, User, Users, LogOut } from 'lucide-react';
import { Link, useLocation } from 'react-router';
import { Button } from './ui/button';
import { useTheme } from 'next-themes';
import { useAuth } from '../context/AuthContext';

export function DesktopNav() {
  const location = useLocation();
  const { theme, setTheme } = useTheme();
  const { isAuthenticated, logout, user } = useAuth();

  const navItems = [
    { icon: Home, label: 'Events', path: '/dashboard/' },
    { icon: Users, label: 'Speakers', path: '/dashboard/speakers' },
    { icon: Network, label: 'Networking', path: '/dashboard/networking' },
    { icon: User, label: 'Profile', path: '/dashboard/profile' },
  ];

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  return (
    <nav className="hidden md:block sticky top-0 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-2">
            <Calendar className="size-6 text-blue-600" />
            <span className="font-semibold text-lg">Event Portal</span>
          </div>

          <div className="flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${isActive
                      ? 'bg-blue-50 dark:bg-blue-950 text-blue-600 dark:text-blue-400'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                    }`}
                >
                  <Icon className="size-4" />
                  <span className="text-sm font-medium">{item.label}</span>
                </Link>
              );
            })}
          </div>

          <div className="flex items-center gap-2">
            {isAuthenticated ? (
              <>
                <span className="text-sm text-gray-600 dark:text-gray-300">
                  {user?.name || user?.email}
                </span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleLogout}
                  className="flex items-center gap-1"
                >
                  <LogOut className="size-4" />
                  Logout
                </Button>
              </>
            ) : (
              <Link to="/login">
                <Button variant="ghost" size="sm">
                  Sign In
                </Button>
              </Link>
            )}
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            >
              {theme === 'dark' ? (
                <Sun className="size-5" />
              ) : (
                <Moon className="size-5" />
              )}
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
}
