import { Calendar, FileText, Home, Network, User, LogOut } from 'lucide-react';
import { Link, useLocation } from 'react-router';
import { useAuth } from '../context/AuthContext';
import { Button } from './ui/button';

export function MobileNav() {
  const location = useLocation();
  const { isAuthenticated, logout, user } = useAuth();

  const navItems = [
    { icon: Home, label: 'Events', path: '/dashboard/' },
    { icon: Calendar, label: 'Agenda', path: '/dashboard/agenda' },
    { icon: Network, label: 'Network', path: '/dashboard/networking' },
    { icon: FileText, label: 'Content', path: '/dashboard/content' },
    { icon: User, label: 'Profile', path: '/dashboard/profile' },
  ];

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 md:hidden z-50 pb-safe">
      <div className="flex justify-around py-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex flex-col items-center py-2 px-3 flex-1 ${isActive
                  ? 'text-blue-600 dark:text-blue-400'
                  : 'text-gray-600 dark:text-gray-400'
                }`}
            >
              <Icon className="size-5 mb-1" />
              <span className="text-xs">{item.label}</span>
            </Link>
          );
        })}
        {isAuthenticated && (
          <button
            onClick={handleLogout}
            className="flex flex-col items-center py-2 px-3 flex-1 text-gray-600 dark:text-gray-400"
          >
            <LogOut className="size-5 mb-1" />
            <span className="text-xs">Logout</span>
          </button>
        )}
      </div>
    </nav>
  );
}
