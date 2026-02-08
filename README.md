# Eventive

Eventive is a comprehensive event management platform built on the [Frappe Framework](https://frappeframework.com/). It provides a complete solution for organizing, managing, and executing events of all sizes, from small meetups to large conferences and exhibitions.

## Features

### Event Management
- **Main Events**: Create and manage multi-day events with detailed information including dates, venues, descriptions, and status tracking
- **Event Sessions**: Schedule and organize sessions with speakers, tracks, and time slots
- **Event Day Tracks**: Manage daily schedules and track-specific programming
- **Venues**: Manage multiple venue locations with capacity and amenity details
- **Event Personnel**: Organize staff and volunteers for event operations

### Ticketing & Registration
- **Event Tickets**: Flexible ticket types with pricing tiers, availability limits, and sales periods
- **Event Registrations**: Manage attendee registrations with status tracking (Draft, Registered, Cancelled, Attended)
- **Check-in Tracking**: Monitor attendee check-ins with real-time reporting
- **Ticket Reports**: Comprehensive reports on ticket sales and check-in rates

### Participant Management
- **Attendee Profiles**: Comprehensive attendee management with personal information, registration history, and preferences
- **Exhibitors**: Manage exhibitor companies with booth assignments and staff members
- **Exhibitor Staff**: Track staff assigned to exhibitor booths
- **Speakers**: Speaker profiles with session assignments and bio information
- **Speaker Sessions**: Link speakers to their sessions with role management

### Content Management
- **Digital Content**: Manage event-related digital assets including documents, videos, and presentations
- **Content Tags**: Organize content with a flexible tagging system

### Merchandise & Sales
- **Merchandise**: Manage event merchandise and souvenirs
- **Booth Packages**: Configure and sell exhibitor booth packages with different tiers

### Networking
- **Match Suggestions**: AI-powered or rule-based attendee matching for networking
- **Networking Messages**: Enable attendee communication through the platform
- **Interest Tags**: Categorize attendees by interests for better networking suggestions
- **Social Media Links**: Connect attendee profiles with social media presence

### Financial Management
- **Event Expenses**: Track and manage event-related expenses
- **Sponsor Tiers**: Manage sponsor levels with associated benefits and pricing
- **Revenue Breakdown**: Detailed revenue analysis by ticket sales, merchandise, and sponsors
- **Financial Performance Report**: Comprehensive financial reporting for events

## Frontend

Eventive includes a modern React-based frontend for attendees and participants to interact with the platform.

### Technology Stack
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Frappe UI** - UI components (Shadcn-inspired)

### Frontend Features
- **Authentication**: Login and registration pages
- **Event Discovery**: Browse and view event details
- **Agenda**: Session scheduling and agenda views
- **Tickets**: Browse and purchase tickets
- **Booking**: Manage event bookings
- **Merchandise**: Browse and purchase event merchandise
- **Speakers**: View speaker profiles and sessions
- **Content**: Access event digital content
- **Networking**: Connect with other attendees
- **Profile**: Manage attendee profiles
- **Feedback**: Submit event feedback
- **Sponsorship**: View and manage sponsorships

### Frontend Pages
- [`Login`](frontend/src/pages/Login.tsx) - User authentication
- [`Register`](frontend/src/pages/Register.tsx) - New user registration
- [`MyEvents`](frontend/src/pages/MyEvents.tsx) - View registered events
- [`EventOverview`](frontend/src/pages/EventOverview.tsx) - Event details and information
- [`Agenda`](frontend/src/pages/Agenda.tsx) - Event schedule and sessions
- [`Ticket`](frontend/src/pages/Ticket.tsx) - Ticket selection and purchase
- [`Booking`](frontend/src/pages/Booking.tsx) - Booking management
- [`Merchandise`](frontend/src/pages/Merchandise.tsx) - Merchandise catalog
- [`Speakers`](frontend/src/pages/Speakers.tsx) - Speaker listings
- [`Content`](frontend/src/pages/Content.tsx) - Digital content library
- [`Networking`](frontend/src/pages/Networking.tsx) - Attendee networking
- [`Profile`](frontend/src/pages/Profile.tsx) - User profile management
- [`Feedback`](frontend/src/pages/Feedback.tsx) - Event feedback submission
- [`Sponsorship`](frontend/src/pages/Sponsorship.tsx) - Sponsorship information

### Frontend Components
- **Navigation**: [`DesktopNav`](frontend/src/components/DesktopNav.tsx), [`MobileNav`](frontend/src/components/MobileNav.tsx)
- **Cards**: [`EventCard`](frontend/src/components/EventCard.tsx), [`SpeakerCard`](frontend/src/components/SpeakerCard.tsx), [`SessionCard`](frontend/src/components/SessionCard.tsx), [`MerchandiseCard`](frontend/src/components/MerchandiseCard.tsx), [`ContentCard`](frontend/src/components/ContentCard.tsx), [`NetworkingMatchCard`](frontend/src/components/NetworkingMatchCard.tsx)
- **UI Components**: Button, Card, Dialog, Input, Label, Progress, Select, Switch, Tabs, Textarea, Badge
- **Layout**: [`RootLayout`](frontend/src/layout/RootLayout.tsx), [`routes`](frontend/src/layout/routes.ts)
- **Services**: [`api.ts`](frontend/src/services/api.ts) - API integration
- **Context**: [`AuthContext`](frontend/src/context/AuthContext.tsx) - Authentication state

## API & Integrations

Eventive provides a comprehensive REST API for external integrations:

- [`events`](eventive/api/events.py) - Event management endpoints
- [`ticket`](eventive/api/ticket.py) - Ticket operations and availability
- [`booking`](eventive/api/booking.py) - Booking management
- [`attendee`](eventive/api/attendee.py) - Attendee profile management
- [`sessions`](eventive/api/sessions.py) - Session scheduling and management
- [`speaker`](eventive/api/speaker.py) - Speaker profile endpoints
- [`content`](eventive/api/content.py) - Digital content management
- [`merchandise`](eventive/api/merchandise.py) - Merchandise operations
- [`networking`](eventive/api/networking.py) - Networking features
- [`auth`](eventive/api/auth.py) - Authentication and authorization

## Installation

### Prerequisites
- Python 3.10+
- Frappe Framework
- Bench CLI tool
- Node.js 18+ (for frontend)
- npm or yarn (for frontend)

### Backend Installation

1. Clone the repository:
```bash
bench get-app https://github.com/your-repo/eventive --branch develop
```

2. Install the app in your bench:
```bash
bench install-app eventive
```

3. Run database migrations:
```bash
bench migrate
```

### Frontend Installation

The frontend is located in the `frontend/` directory.

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

### Running Both Backend and Frontend

For development, you'll typically run both the Frappe bench and the frontend dev server:

```bash
# Terminal 1 - Start Frappe bench
bench start

# Terminal 2 - Start frontend
cd frontend
npm run dev
```

The frontend will typically run on `http://localhost:5173` and proxy API requests to the Frappe bench server.

## Contributing

We welcome contributions to Eventive! This project uses `pre-commit` for code quality. Please install and enable it:

```bash
cd apps/eventive
pre-commit install
```

### Code Standards

Pre-commit is configured with the following tools:
- **ruff** - Fast Python linter
- **eslint** - JavaScript linting
- **prettier** - Code formatting
- **pyupgrade** - Modern Python syntax

For frontend code:
```bash
cd frontend
npm run lint   # Run ESLint
npm run format # Run Prettier
```

## CI/CD

GitHub Actions workflows are configured for:
- **CI**: Runs unit tests on every push to `develop` branch
- **Linters**: Runs Frappe Semgrep Rules and pip-audit on pull requests

## Project Structure

```
eventive/
├── api/                    # REST API endpoints
│   ├── auth.py
│   ├── attendee.py
│   ├── booking.py
│   ├── content.py
│   ├── events.py
│   ├── merchandise.py
│   ├── networking.py
│   ├── sessions.py
│   ├── speaker.py
│   └── ticket.py
├── eventive/               # Core event management module
│   ├── doctype/
│   │   ├── booth_package/
│   │   ├── content_tag/
│   │   ├── digital_content/
│   │   ├── event_day_track/
│   │   ├── event_expense/
│   │   ├── event_feedback/
│   │   ├── event_host/
│   │   ├── event_personnel/
│   │   ├── event_session/
│   │   ├── event_task/
│   │   ├── main_event/
│   │   ├── merchandise/
│   │   ├── sponsor_tier/
│   │   ├── talk_speaker/
│   │   └── venue/
│   └── report/
│       ├── financial_performance_report/
│       ├── revenue_breakdown/
│       └── ticket_&_check_in_rate/
├── events/                 # Event-related utilities
├── exhibitor/              # Exhibitor management
├── networking/             # Networking features
│   └── doctype/
│       ├── interest_tags/
│       ├── match_suggestion/
│       ├── networking_message/
│       └── social_media_links/
├── participants/           # Participant management
│   └── doctype/
│       ├── attendee_profile/
│       ├── exhibitor/
│       ├── exhibitor_staff/
│       ├── speaker/
│       ├── speaker_profile/
│       ├── speaker_sessions/
│       └── sponsor/
├── ticketing/              # Ticketing system
│   └── doctype/
│       ├── event_ticket/
│       └── event_registration/
└── hooks.py                # App hooks and configuration

frontend/                  # React frontend application
├── public/                 # Static assets
├── src/
│   ├── assets/            # Images and static resources
│   ├── components/        # React components
│   │   ├── ui/           # Reusable UI components
│   │   ├── ContentCard.tsx
│   │   ├── DesktopNav.tsx
│   │   ├── EventCard.tsx
│   │   ├── MerchandiseCard.tsx
│   │   ├── MessageDialog.tsx
│   │   ├── MobileNav.tsx
│   │   ├── NetworkingMatchCard.tsx
│   │   ├── SessionCard.tsx
│   │   └── SpeakerCard.tsx
│   ├── context/          # React context providers
│   │   └── AuthContext.tsx
│   ├── layout/            # Layout components and routes
│   │   ├── RootLayout.tsx
│   │   └── routes.ts
│   ├── pages/            # Page components
│   │   ├── Agenda.tsx
│   │   ├── Booking.tsx
│   │   ├── Content.tsx
│   │   ├── EventOverview.tsx
│   │   ├── Feedback.tsx
│   │   ├── Login.tsx
│   │   ├── Merchandise.tsx
│   │   ├── MyEvents.tsx
│   │   ├── Networking.tsx
│   │   ├── Profile.tsx
│   │   ├── Register.tsx
│   │   ├── Speakers.tsx
│   │   ├── Sponsorship.tsx
│   │   └── Ticket.tsx
│   ├── services/          # API services and utilities
│   │   ├── api.ts
│   │   └── mockData.ts
│   ├── App.tsx           # Main application component
│   ├── index.css         # Global styles
│   ├── main.tsx          # Application entry point
│   ├── tailwind.css      # Tailwind CSS styles
│   └── theme.css         # Theme configuration
├── eslint.config.js       # ESLint configuration
├── index.html            # HTML entry point
├── package.json          # npm dependencies
├── tsconfig.app.json     # TypeScript config for app
├── tsconfig.json         # TypeScript base config
├── tsconfig.node.json    # TypeScript config for Node
└── vite.config.ts        # Vite configuration
```

## License

MIT License - see LICENSE file for details.

## Support

For issues and feature requests, please use the GitHub issue tracker.

