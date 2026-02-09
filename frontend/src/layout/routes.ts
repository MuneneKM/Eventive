import { createBrowserRouter } from 'react-router';
import { ProtectedRootLayout } from './ProtectedRootLayout';
import { PublicLayout } from '../components/RouteWrappers';
import { Home } from '../pages/Home';
import { EventOverview } from '../pages/EventOverview';
import { Agenda } from '../pages/Agenda';
import { Speakers } from '../pages/Speakers';
import { Content } from '../pages/Content';
import { Networking } from '../pages/Networking';
import { Merchandise } from '../pages/Merchandise';
import { Profile } from '../pages/Profile';
import { Feedback } from '../pages/Feedback';
import { Booking } from '../pages/Booking';
import { Ticket } from '../pages/Ticket';
import { Register } from '../pages/Register';
import { Login } from '../pages/Login';
import { Sponsorship } from '../pages/Sponsorship';
import { NotFound } from '../pages/NotFound';

export const router = createBrowserRouter([
  // Public routes (accessible by anyone)
  {
    path: '/',
    Component: PublicLayout,
    children: [
      { index: true, Component: Home },
    ],
  },
  {
    path: '/login',
    Component: PublicLayout,
    children: [
      { index: true, Component: Login },
    ],
  },
  {
    path: '/register',
    Component: PublicLayout,
    children: [
      { index: true, Component: Register },
    ],
  },

  // Protected routes (require authentication)
  {
    path: '/dashboard',
    Component: ProtectedRootLayout,
    children: [
      { index: true, Component: Home },
      { path: 'event/:eventId', Component: EventOverview },
      { path: 'event/:eventId/feedback', Component: Feedback },
      { path: 'event/:eventId/book', Component: Booking },
      { path: 'event/:eventId/ticket', Component: Ticket },
      { path: 'event/:eventId/sponsorship', Component: Sponsorship },
      { path: 'agenda', Component: Agenda },
      { path: 'speakers', Component: Speakers },
      { path: 'content', Component: Content },
      { path: 'networking', Component: Networking },
      { path: 'merchandise', Component: Merchandise },
      { path: 'profile', Component: Profile },
    ],
  },

  // 404 Not Found
  {
    path: '*',
    Component: NotFound,
  },
]);
