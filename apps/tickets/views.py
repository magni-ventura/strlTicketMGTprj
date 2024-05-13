import random
import string
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import get_user_model
from .form import CreateTicketForm, AssignTicketForm
from.models import Ticket



# Create your views here.

"""
For Customers
"""
#Creating a Ticket

def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            while not var.ticket_id:
                id = ''.join(random.choices(string.digits, k=6) )
                try:
                    var.ticket_id = id
                    var.save()
                    #send email function
                    subject = f'{var.ticket_title} #{var.ticket_id}'
                    message = 'Thank you for creating a ticket we would assign an engineer ASAP.'
                    email_from = ''
                    recipient_list = [request.user.email, ]
                    send_mail(subject, message, email_from, recipient_list)
                    messages.success(request, 'Your ticket Successfully Created an Engineer will be assigned to it soon.')
                    return redirect('customer-active-tickets')
                    #break
                except IntegrityError:
                    continue
        else:
            messages.warning(request, 'something went wrong. Please check form inputs for errors and try again.')
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form':form}
        return render(request, 'ticket/create-ticket.html', context)

#customer can view all customer_active_tickets  

def customer_active_tickets(request):
    tickets = Ticket.objects.filter(customer=request.user, is_resolved=False).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request, 'ticket/customer_active_tickets.html', context)


#customer can view all customer_resolved_tickets  

def customer_resolved_tickets(request):
    tickets = Ticket.objects.filter(customer=request.user, is_resolved=True).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request, 'ticket/customer_resolved_tickets.html', context)


#engineer can view all engineer_active_tickets  

def engineer_active_tickets(request):
    tickets = Ticket.objects.filter(engineer=request.user, is_resolved=False).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request, 'ticket/engineer_active_tickets.html', context)


#engineer can view all resolved_tickets  

def engineer_resolved_tickets(request):
    tickets = Ticket.objects.filter(engineer=request.user, is_resolved=True).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request, 'ticket/engineer_resolved_tickets.html', context)


#Assign tickets

def assign_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.method == 'POST':
        form = AssignTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_assigned_to_engineer = True
            var.status = 'Active'
            var.save()
            messages.success(request, f'Ticket has been assigned to {var.engineer}')
            return redirect ('ticket-queue')
        else:
            messages.warning(request, 'Something went Wrong. Please check form input')
            return redirect('assign-tickets')#check l8r
    else:
        form = AssignTicketForm(instance=ticket)
        form.fields['engineer'].queryset = user.objects.filter(is_engineer=True)
        context = {'form':form, 'ticket':ticket}
        return render(request, 'ticket/assign-ticket.html')



#View ticket details

def ticket_details(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    context = {'ticket': ticket, 'ticket_per_user': ticket_per_user}
    return render(request, 'ticket/ticket-details.html', context)




#view ticket queue(admins only)

def ticket_queue(request):
    tickets = Ticket.objects.filter(is_assigned_to_engineer=False)
    context = {'tickets':tickets}
    return render(request, 'ticket/ticket-queue.html', context)

# Accept a Ticket from queue

def accept_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.assigned_to = request.user
    ticket.ticket_status = 'Active'
    ticket.accepted_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Ticket has been accepted and will be resolved as soon as possible.')
    return redirect('workspace')

# Close a Ticket

def close_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.ticket_status = 'Completed'
    ticket.is_resolved=True
    ticket.closed_date = datetime.datetime.now()
    ticket.save()
    messages.info(request, 'Ticket has been resolved.')
    return redirect('ticket-queue')

# View ticket engineer is working on

def work_space(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=False)
    context = {'tickets': tickets}
    return render(request, 'ticket/workspace.html', context)

# All closed/resolved tickets

def all_closed_tickets(request):
    tickets = Tickets.objects.filter(assigned_to=request.user, is_resolved=True)
    context = {'ticket': ticket}
    return render(request, 'ticket/all_closed_ticket.html', context)



#Updating a Ticket

def update_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if not ticket.is_resolved:
        if request.method == 'POST':
            form = UpdateTicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                messages.info(request, 'Your Ticket Info is Successfully Updated')
                return redirect('dashboard')
            else:
                messages.warning(request, 'something went wrong. Please check form inputs and try again.')
                #return redirect('update-ticket')
        else:
            form = UpdateTicketForm(instance=ticket)
            context = {'form': form}
            return render(request, 'ticket/update-ticket.html', context)
    else:
        messages.warning(request, 'You cannot make any changes')
        return redirect('dashboard')


def resolved_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.method == 'POSt':
        rs = request.POST.get('rs')
        ticket.resolution_steps = rs
        ticket.is_resolved=True
        ticket.status = 'Resolved'
        ticket.save()
        messages.success(request, 'Ticket is now resolved and closed')
        return redirect('dashboard')