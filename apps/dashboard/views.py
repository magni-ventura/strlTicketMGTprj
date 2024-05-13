from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.

# This is a reference snippet of code from magniTicketMGTprj/dashboard/views.py:

"""
    This function returns the dashboard page for the user based on their role.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The dashboard page for the user.

"""

@login_required
def dashboard(request):
    if request.user.is_customer:
        # Get the number of tickets assigned to the customer
        tickets = Ticket.objects.filter(customer=request.user).count()
        # Get the number of active tickets assigned to the customer
        active_tickets = Ticket.objects.filter(customer=request.user, is_resolved=False).count()
        # Get the number of closed tickets assigned to the customer
        closed_tickets = Ticket.objects.filter(customer=request.user, is_resolved=True).count()
        # Create a context dictionary with the ticket counts
        context = {
            'tickets': tickets,
            'active_tickets': active_tickets,
            'closed_tickets': closed_tickets
        }
        # Render the customer dashboard template with the context
        return render(request, 'dashboard/customer_dashboard.html', context)

    elif request.user.is_engineer:
        # Get the number of tickets assigned to the engineer
        tickets = Ticket.objects.filter(engineer=request.user).count()
        # Get the number of active tickets assigned to the engineer
        active_tickets = Ticket.objects.filter(engineer=request.user, is_resolved=False).count()
        # Get the number of closed tickets assigned to the engineer
        closed_tickets = Ticket.objects.filter(engineer=request.user, is_resolved=True).count()
        # Create a context dictionary with the ticket counts
        context = {
            'tickets': tickets,
            'active_tickets': active_tickets,
            'closed_tickets': closed_tickets
        }
        # Render the engineer dashboard template with the context
        return render(request, 'dashboard/engineer_dashboard.html', context)

    elif request.user.is_superuser:
        # Render the admin dashboard template
        return render(request, 'dashboard/admin_dashboard.html')