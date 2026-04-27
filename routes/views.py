from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Count, Q

from .models import Station, Route


def index(request):
    """List all routes with optional search/filter by origin or destination."""
    query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', 'city').strip()
    routes = Route.objects.select_related('origin', 'destination').annotate(
        passenger_count=Count('passengers')
    )
    if query:
        routes = routes.filter(
            Q(origin__name__icontains=query) |
            Q(origin__city__icontains=query) |
            Q(destination__name__icontains=query) |
            Q(destination__city__icontains=query)
        )
    popular_route = routes.order_by('-passenger_count', 'duration').first()

    if sort == 'duration_asc':
        order_by = ('duration', 'origin__city', 'origin__name')
    elif sort == 'duration_desc':
        order_by = ('-duration', 'origin__city', 'origin__name')
    elif sort == 'passengers_desc':
        order_by = ('-passenger_count', 'origin__city', 'origin__name')
    elif sort == 'passengers_asc':
        order_by = ('passenger_count', 'origin__city', 'origin__name')
    elif sort == 'route':
        order_by = ('origin__name', 'destination__name')
    else:
        sort = 'city'
        order_by = ('origin__city', 'origin__name', 'destination__city', 'destination__name')

    routes = routes.order_by(*order_by)

    route_count = Route.objects.count()
    station_count = Station.objects.count()
    total_bookings = Route.objects.aggregate(
        total_bookings=Count('passengers')
    )['total_bookings'] or 0
    user_booking_count = (
        request.user.booked_routes.count()
        if request.user.is_authenticated
        else 0
    )
    return render(request, 'routes/index.html', {
        'routes': routes,
        'query': query,
        'sort': sort,
        'route_count': route_count,
        'station_count': station_count,
        'total_bookings': total_bookings,
        'user_booking_count': user_booking_count,
        'popular_route': popular_route,
    })


def route_detail(request, route_id):
    """Show route info, passengers, and book/unbook controls."""
    route = get_object_or_404(
        Route.objects.select_related('origin', 'destination'),
        pk=route_id
    )
    passenger_list = route.passengers.all()
    is_passenger = (
        request.user.is_authenticated and
        route.passengers.filter(pk=request.user.pk).exists()
    )
    return render(request, 'routes/route_detail.html', {
        'route': route,
        'passengers': passenger_list,
        'is_passenger': is_passenger,
    })


def station_detail(request, station_id):
    """Show all routes departing from and arriving at a station."""
    station = get_object_or_404(Station, pk=station_id)
    departures = station.departures.select_related('destination').annotate(
        passenger_count=Count('passengers')
    )
    arrivals = station.arrivals.select_related('origin').annotate(
        passenger_count=Count('passengers')
    )
    return render(request, 'routes/station_detail.html', {
        'station': station,
        'departures': departures,
        'arrivals': arrivals,
    })


@login_required
@require_POST
def book(request, route_id):
    """Add the logged-in user to the route's passengers."""
    route = get_object_or_404(Route, pk=route_id)
    if not route.passengers.filter(pk=request.user.pk).exists():
        route.passengers.add(request.user)
        messages.success(request, 'Seat booked successfully!')
    return redirect('route_detail', route_id=route.id)


@login_required
@require_POST
def unbook(request, route_id):
    """Remove the logged-in user from the route's passengers."""
    route = get_object_or_404(Route, pk=route_id)
    if route.passengers.filter(pk=request.user.pk).exists():
        route.passengers.remove(request.user)
        messages.info(request, 'Booking cancelled.')
    return redirect('route_detail', route_id=route.id)


@login_required
def my_routes(request):
    """Show all routes the logged-in user has booked."""
    routes = request.user.booked_routes.select_related(
        'origin', 'destination'
    ).annotate(passenger_count=Count('passengers'))
    return render(request, 'routes/my_routes.html', {
        'routes': routes,
    })


def register_view(request):
    """Register a new user account."""
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome aboard, {user.username}!')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'routes/register.html', {'form': form})
