import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { Calendar, MapPin, User, ArrowRight, Search, Clock, Info, X } from 'lucide-react';
import { eventsAPI } from '../services/api';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Badge } from '../components/ui/badge';
import { useAuth } from '../context/AuthContext';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
} from '../components/ui/dialog';

interface Event {
    name: string;
    event_name: string;
    banner_image: string;
    start_date: string;
    end_date: string;
    venue_name: string;
    host_name: string;
    ticket_type: 'Regular' | 'VIP';
    status: 'Upcoming' | 'Ongoing' | 'Completed';
    qrCode: string;
    description?: string;
    vipBenefits?: string[];
}

export function Home() {
    const navigate = useNavigate();
    const { isAuthenticated } = useAuth();
    const [events, setEvents] = useState<Event[]>([]);
    const [filteredEvents, setFilteredEvents] = useState<Event[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    const [searchQuery, setSearchQuery] = useState('');
    const [statusFilter, setStatusFilter] = useState<string>('all');
    const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                setIsLoading(true);
                const response = await eventsAPI.getAll();
                const eventsData = response.data.message || [];
                setEvents(eventsData);
                setFilteredEvents(eventsData);
            } catch (err) {
                console.error('Failed to fetch events:', err);
                setError('Failed to load events. Please try again later.');
            } finally {
                setIsLoading(false);
            }
        };

        fetchEvents();
    }, []);

    useEffect(() => {
        // Filter events based on search query and status filter
        let filtered = [...events];

        if (searchQuery) {
            const query = searchQuery.toLowerCase();
            filtered = filtered.filter(
                (event) =>
                    event.event_name.toLowerCase().includes(query) ||
                    event.venue_name.toLowerCase().includes(query) ||
                    event.host_name.toLowerCase().includes(query)
            );
        }

        if (statusFilter !== 'all') {
            filtered = filtered.filter((event) => event.status === statusFilter);
        }

        setFilteredEvents(filtered);
    }, [searchQuery, statusFilter, events]);

    const handleOpenEvent = (event: Event) => {
        setSelectedEvent(event);
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
        setSelectedEvent(null);
    };

    const handleRegisterClick = () => {
        if (!isAuthenticated) {
            navigate('/login');
        } else if (selectedEvent) {
            navigate(`/dashboard/event/${selectedEvent.name}/book`);
        }
    };

    const handleLearnMoreClick = () => {
        if (!isAuthenticated) {
            navigate('/login');
        } else if (selectedEvent) {
            navigate(`/dashboard/event/${selectedEvent.name}`);
        }
    };

    const statusCounts = {
        all: events.length,
        upcoming: events.filter((e) => e.status === 'Upcoming').length,
        ongoing: events.filter((e) => e.status === 'Ongoing').length,
        completed: events.filter((e) => e.status === 'Completed').length,
    };

    if (isLoading) {
        return (
            <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
                <div className="max-w-7xl mx-auto px-4 py-8">
                    <div className="flex items-center justify-center h-64">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
                <div className="max-w-7xl mx-auto px-4 py-8">
                    <div className="text-center">
                        <p className="text-red-600 dark:text-red-400 mb-4">{error}</p>
                        <Button onClick={() => window.location.reload()}>Retry</Button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
            {/* Hero Section */}
            <div className="dark:bg-blue-900/20 bg-gray-800 text-white">
                <div className="max-w-7xl mx-auto px-4 py-16">
                    <div className="max-w-3xl">
                        <h1 className="text-4xl md:text-5xl font-bold mb-4">
                            Discover Amazing Events
                        </h1>
                        <p className="text-xl text-blue-100 mb-8">
                            Find and register for conferences, workshops, and networking opportunities
                        </p>

                        {!isAuthenticated ? (
                            <div className="flex flex-wrap gap-4">
                                <Button
                                    size="lg"
                                    onClick={() => navigate('/register')}
                                    className="bg-white text-blue-600 hover:bg-blue-50"
                                >
                                    Create an Account
                                </Button>
                                <Button
                                    size="lg"
                                    variant="outline"
                                    onClick={() => navigate('/login')}
                                    className="border-white text-white hover:bg-white/10"
                                >
                                    Sign In
                                </Button>
                            </div>
                        ) : (
                            <div className="flex items-center gap-4">
                                <p className="text-lg">Welcome back!</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Main Content */}
            <div className="max-w-7xl mx-auto px-4 py-8">
                {/* Search and Filter Section */}
                <div className="mb-8">
                    <div className="flex flex-col md:flex-row gap-4 mb-6">
                        <div className="relative flex-1">
                            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 size-5" />
                            <Input
                                type="text"
                                placeholder="Search events by name, venue, or organizer..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="pl-10"
                            />
                        </div>
                        <div className="flex gap-2">
                            <Button
                                variant={statusFilter === 'all' ? 'default' : 'outline'}
                                onClick={() => setStatusFilter('all')}
                            >
                                All ({statusCounts.all})
                            </Button>
                            <Button
                                variant={statusFilter === 'Upcoming' ? 'default' : 'outline'}
                                onClick={() => setStatusFilter('Upcoming')}
                            >
                                Upcoming ({statusCounts.upcoming})
                            </Button>
                            <Button
                                variant={statusFilter === 'Ongoing' ? 'default' : 'outline'}
                                onClick={() => setStatusFilter('Ongoing')}
                            >
                                Ongoing ({statusCounts.ongoing})
                            </Button>
                        </div>
                    </div>

                    {/* Events Grid */}
                    {filteredEvents.length > 0 ? (
                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                            {filteredEvents.map((event) => (
                                <div
                                    key={event.name}
                                    className="bg-white dark:bg-blue-900/20  rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-shadow cursor-pointer"
                                    onClick={() => handleOpenEvent(event)}
                                >
                                    <div className="h-48 overflow-hidden">
                                        <img
                                            src={event.banner_image}
                                            alt={event.event_name}
                                            className="w-full h-full object-cover"
                                        />
                                    </div>
                                    <div className="p-6">
                                        <div className="flex gap-2 mb-3">
                                            <Badge variant={
                                                event.status === 'Upcoming' ? 'default' :
                                                    event.status === 'Ongoing' ? 'secondary' : 'outline'
                                            }>
                                                {event.status}
                                            </Badge>
                                            {event.ticket_type === 'VIP' && (
                                                <Badge className="bg-gradient-to-r from-amber-500 to-yellow-500 text-white">
                                                    VIP
                                                </Badge>
                                            )}
                                        </div>
                                        <h3 className="text-xl font-semibold mb-4">{event.event_name}</h3>
                                        <div className="space-y-2 text-sm text-gray-600 dark:text-gray-300">
                                            <div className="flex items-center gap-2">
                                                <Calendar className="size-4" />
                                                <span>
                                                    {new Date(event.start_date).toLocaleDateString('en-US', {
                                                        month: 'short',
                                                        day: 'numeric',
                                                    })}
                                                    {' - '}
                                                    {new Date(event.end_date).toLocaleDateString('en-US', {
                                                        month: 'short',
                                                        day: 'numeric',
                                                        year: 'numeric',
                                                    })}
                                                </span>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <MapPin className="size-4" />
                                                <span>{event.venue_name}</span>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <User className="size-4" />
                                                <span>{event.host_name}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-12">
                            <Calendar className="size-12 mx-auto text-gray-300 mb-4" />
                            <p className="text-gray-600 dark:text-gray-400 text-lg">
                                No events found
                            </p>
                            <p className="text-gray-500 mb-4">
                                {searchQuery || statusFilter !== 'all'
                                    ? 'Try adjusting your search or filters'
                                    : 'Check back later for new events'}
                            </p>
                            {(searchQuery || statusFilter !== 'all') && (
                                <Button
                                    variant="outline"
                                    onClick={() => {
                                        setSearchQuery('');
                                        setStatusFilter('all');
                                    }}
                                >
                                    Clear Filters
                                </Button>
                            )}
                        </div>
                    )}
                </div>

                {/* Registration Info Section */}
                {!isAuthenticated && (
                    <div className="mt-12 bg-gray-50 dark:bg-blue-900/20 rounded-xl p-8 text-center">
                        <h2 className="text-2xl font-bold mb-4">Ready to Register?</h2>
                        <p className="text-gray-600 dark:text-gray-300 mb-6 max-w-2xl mx-auto">
                            Create an account to register for events, book sessions, network with attendees,
                            and access exclusive content.
                        </p>
                        <Button size="lg" onClick={() => navigate('/register')}>
                            Create Your Account <ArrowRight className="ml-2 size-5" />
                        </Button>
                    </div>
                )}
            </div>

            {/* Event Overview Modal */}
            <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
                <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
                    <DialogHeader>
                        <DialogTitle className="text-2xl">{selectedEvent?.event_name}</DialogTitle>
                    </DialogHeader>

                    {selectedEvent && (
                        <div className="space-y-6">
                            {/* Banner */}
                            <div className="h-48 overflow-hidden rounded-lg">
                                <img
                                    src={selectedEvent.banner_image}
                                    alt={selectedEvent.event_name}
                                    className="w-full h-full object-cover"
                                />
                            </div>

                            {/* Status and Type */}
                            <div className="flex gap-2">
                                <Badge variant={
                                    selectedEvent.status === 'Upcoming' ? 'default' :
                                        selectedEvent.status === 'Ongoing' ? 'secondary' : 'outline'
                                }>
                                    {selectedEvent.status}
                                </Badge>
                                {selectedEvent.ticket_type === 'VIP' && (
                                    <Badge className="bg-gradient-to-r from-amber-500 to-yellow-500 text-white">
                                        VIP Access
                                    </Badge>
                                )}
                            </div>

                            {/* Event Details */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="flex items-center gap-3 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                                    <Calendar className="size-5 text-blue-600" />
                                    <div>
                                        <p className="text-sm text-gray-600 dark:text-gray-400">Date</p>
                                        <p className="font-medium">
                                            {new Date(selectedEvent.start_date).toLocaleDateString('en-US', {
                                                month: 'long',
                                                day: 'numeric',
                                            })}
                                            {' - '}
                                            {new Date(selectedEvent.end_date).toLocaleDateString('en-US', {
                                                month: 'long',
                                                day: 'numeric',
                                                year: 'numeric',
                                            })}
                                        </p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-3 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                                    <MapPin className="size-5 text-blue-600" />
                                    <div>
                                        <p className="text-sm text-gray-600 dark:text-gray-400">Venue</p>
                                        <p className="font-medium">{selectedEvent.venue_name}</p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-3 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                                    <User className="size-5 text-blue-600" />
                                    <div>
                                        <p className="text-sm text-gray-600 dark:text-gray-400">Organizer</p>
                                        <p className="font-medium">{selectedEvent.host_name}</p>
                                    </div>
                                </div>
                            </div>

                            {/* Description */}
                            {selectedEvent.description && (
                                <div>
                                    <h3 className="text-lg font-semibold mb-2">About This Event</h3>
                                    <div
                                        className="text-gray-600 dark:text-gray-300"
                                        dangerouslySetInnerHTML={{ __html: selectedEvent.description }}
                                    />
                                </div>
                            )}

                            {/* VIP Benefits */}
                            {selectedEvent.vipBenefits && selectedEvent.vipBenefits.length > 0 && (
                                <div>
                                    <h3 className="text-lg font-semibold mb-2">VIP Benefits</h3>
                                    <ul className="list-disc list-inside space-y-1 text-gray-600 dark:text-gray-300">
                                        {selectedEvent.vipBenefits.map((benefit, index) => (
                                            <li key={index}>{benefit}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {/* Action Buttons */}
                            <div className="flex flex-col sm:flex-row gap-4 pt-4 border-t">
                                <Button
                                    size="lg"
                                    onClick={handleRegisterClick}
                                    className="flex-1"
                                >
                                    Register for Event
                                </Button>
                                <Button
                                    size="lg"
                                    variant="outline"
                                    onClick={handleLearnMoreClick}
                                    className="flex-1"
                                >
                                    Learn More
                                </Button>
                            </div>

                            {!isAuthenticated && (
                                <p className="text-sm text-center text-gray-500">
                                    You need to be logged in to register or view full event details
                                </p>
                            )}
                        </div>
                    )}
                </DialogContent>
            </Dialog>
        </div>
    );
}
