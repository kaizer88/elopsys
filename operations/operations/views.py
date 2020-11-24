from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from models import OperationsUser, Region, Branch, BaseTicket
from forms import OperationsUserForm, OperationsUserFilterForm, RegionForm, ServiceProviderImportForm
from forms import BranchForm, DownloadsFilterForm, TicketFilterForm, TicketForm, DistrictImportForm
from forms import EditUserForm
from fleet_management.exporter import extract_user_data, extract_tickets_data
from operations.models import *
from fleet_management.importer import import_service_provider_data, import_district_data
from lib.file_handler import file_download
import threading
import datetime
from django.contrib import messages

@login_required
def about(request): 
    return render(request, "about.html", {})

@login_required
def home(request, template='operations/home.html'):
    
    return render(request, template, {})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_management) 
def users(request, fleet_administrators=False, template="users/users.html"):
    
    context = {}
    user_filter_form = OperationsUserFilterForm(request.POST or None)
    if fleet_administrators:
        users = OperationsUser.objects.filter(groups__name='Fleet Administrators')
        title = "Fleet Administrators"
    else:
        users = OperationsUser.objects.all()
        title = "Users"

    # if not request.user.is_superuser:
    #     return redirect(reverse('logout'))

    if u'search' in request.POST:
        if user_filter_form.is_valid():
            users = user_filter_form.filter(users)
            if len(set(user_filter_form.cleaned_data.values())) > 1:
                context['reset_button'] = True            

    if u'extract' in request.POST:
        if user_filter_form.is_valid(): 
            users = user_filter_form.filter(users)
            download_thread = threading.Thread(target=extract_user_data, 
                                               args=(request.user, 'all_users', users, 
                                                     user_filter_form.cleaned_data))
            download_thread.start()
            messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')
            if len(set(user_filter_form.cleaned_data.values())) > 1:
                context['reset_button'] = True

    
    context['users'] = users
    context['title'] = title
    context['user_filter_form'] = user_filter_form
    return render(request, template, context)

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_management) 
def user_edit(request, user_id=None, template="users/user_edit.html"):
    context = {}
    user = OperationsUser.objects.get(pk=user_id) if user_id else None
    user_form = OperationsUserForm(request.POST or None, instance=user)

    # if not request.user.is_superuser:
    #     return redirect(reverse('logout'))

    if u'save' in request.POST  and  user_form.is_valid():
        user = user_form.save()
        next = request.POST.get('next', '/')
            
        return HttpResponseRedirect(next)

    if u'cancel' in request.POST:
        next = request.POST.get('next', '/')            
        return HttpResponseRedirect(next)
        

    context['form'] = user_form
    context['user'] = user
    return render(request, template, context)

        

@login_required
def view_regions(request, template="operations/view_regions.html"):
    context = {}

    regions = Region.objects.all().order_by('code')
    
    context['regions'] = regions

    return render(request, template, context) 

@login_required
def view_branches(request, template="operations/view_branches.html"):
    context = {}

    branches = Branch.objects.all()
    
    context['branches'] = branches

    return render(request, template, context)


@login_required
def downloads_list(request, template="operations/downloads.html"):
    context = {}
   
    downloads = Document.objects.filter(file_type__in=['Download']).order_by("-created_at")
    filter_form = DownloadsFilterForm(request.POST or None)
    if u'search' in request.POST:
        if filter_form.is_valid():
            downloads = filter_form.filter(downloads)

    context['downloads'] = downloads
    context['dl_user'] = request.user
    context['filter_form'] = filter_form

    return render(request, template, context)


def file_download_task(request, file_id):
    saved_file = Document.objects.get(pk=file_id)
    return file_download(file=saved_file)


@login_required
def view_tickets(request, template="operations/view_tickets.html"):
    
    context = {}
    ticket_filter_form = TicketFilterForm(request.POST or None)

    tickets = BaseTicket.objects.all()

    if u'search' in request.POST:
        if ticket_filter_form.is_valid():
            tickets = ticket_filter_form.filter(tickets)

    if u'extract' in request.POST:
        if ticket_filter_form.is_valid(): 
            tickets = ticket_filter_form.filter(tickets)
            download_thread = threading.Thread(target=extract_tickets_data, 
                                               args=(request.user, 'all_tickets', tickets, 
                                                     ticket_filter_form.cleaned_data))
            download_thread.start()
            messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')
    
    context['tickets'] = tickets
    context['ticket_filter_form'] = ticket_filter_form
    return render(request, template, context)

@login_required
def edit_ticket(request,  ticket_id=None, template="operations/edit_ticket.html", context=None):

    context = context or {}
    ticket = None

    if ticket_id:
        ticket = BaseTicket.objects.get(pk=ticket_id)
        ticket_form = TicketForm(
            request.POST or None, instance=ticket)
    else:
        ticket_form = TicketForm(request.POST or None)

    if ticket_form.is_valid():
        ticket = ticket_form.save(commit=False)
        if ticket_id:      
            ticket.created_by = request.user
            ticket.save()
            obj = BaseTicket.objects.get(pk=ticket_id)
            messages.success(request, 'Ticket %s is updated' %(obj.number))
        else:
            ticket.created_by = request.user
            ticket.number = generate_ticket_ref()
            ticket.save()
            objj = BaseTicket.objects.latest('id')
            messages.success(request, 'Ticket %s is created' %(objj.number))


        return redirect(reverse('view_tickets'))

    context['form'] = ticket_form
    context['ticket'] = ticket
    
    return render(request, template, context)

def generate_ticket_ref():

    ticket = None
    ticket = BaseTicket.objects.all()
    date = datetime.datetime.now().strftime('%d%m%Y')

    if ticket:
        obj = BaseTicket.objects.latest('id')
        get_date = obj.created_at.strftime('%d%m%Y')
        get_number = obj.number
        get_index = get_number[11:]
        if get_date == date and get_index == '0':    
            ref=1
        elif get_date == date and get_index != '0':
            get_num = int(get_index)               
            ref = get_num+1
        else:                
            ref = 0
    else:
        ref = 0

    ticket_division = "FL"
    # date = datetime.datetime.now().strftime('%d%m%Y')
    if BaseTicket.objects.filter(number=ref).count() > 0:
        generate_ticket_ref()
    return ticket_division + date +'-'+str(ref)

@login_required
def service_provider_uploads(request, template="operations/service_provider_uploads.html"):
    context = {}

    form = ServiceProviderImportForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        import_service_provider_data(request.user, form.cleaned_data.get('service_provider_file'))

    context['form'] = form

    return render(request, template, context)

@login_required
def district_uploads(request, template="operations/district_uploads.html"):
    context = {}

    form = DistrictImportForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        import_district_data(request.user, form.cleaned_data.get('district_file'))

    context['form'] = form
    return render(request, template, context)

@login_required
def user_profile(request, user_id=None, template="users/user_profile.html"):
    context = {}
    user = OperationsUser.objects.get(pk=user_id) if user_id else None
    user_form = EditUserForm(request.POST or None, instance=user)


    if u'save' in request.POST  and  user_form.is_valid():
        user = user_form.save()
        next = request.POST.get('next', '/')           
        return HttpResponseRedirect(next)

    if u'cancel' in request.POST:
        next = request.POST.get('next', '/')            
        return HttpResponseRedirect(next)
        
    context['form'] = user_form
    context['user'] = user
    return render(request, template, context)