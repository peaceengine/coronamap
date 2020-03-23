from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Statement, Response, UserGeoLocation, Hashtag
from django.utils import timezone
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from django.template import loader

from django.views.generic.edit import FormView
from statements.forms import LookupForm
#from django.shortcuts import render_to_response

def home(request):
    # latest_statement_list = Statement.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.statement_text for q in latest_statement_list])
    # return HttpResponse(output)
    # statements = Statement.objects.all().order_by('-pub_date') # gets all the projects out of the database
    # return render(request, 'statements/home.html', {'statements':statements})

    latest_statement_list = Statement.objects.all().order_by('-pub_date')[:5] # gets all the projects out of the database
    template = loader.get_template('statements/home.html') #statements/
    context = {'latest_statement_list':latest_statement_list,}
    return HttpResponse(template.render(context, request))
   # return render(request, 'statements/home.html', {'latest_statement_list':latest_statement_list}) #statements/


#    return render(request, 'statements/home.html', {'statements':statements})
#    output = ', '.join([q.statement_text for q in latest_statement_list])
#    return HttpResponse(output)

@login_required(login_url="/accounts/signup")
def create(request):
    if request.method == 'POST':
        if request.POST['statement_text']:
            statement = Statement()
            statement.statement_text = request.POST['statement_text']
            statement.pub_date = timezone.datetime.now()
            statement.creator = request.user
            if request.FILES['icon_disagree']:
                statement.iconDisagree = request.FILES['icon_disagree']
            if request.FILES['icon_agree']:
                statement.iconAgree = request.FILES['icon_agree']
            if request.FILES['icon']:
                statement.icon = request.FILES['icon']
            statement.save() # inserts it into the database

            return redirect('/statements/' + str(statement.id)) # show user the Statement
        else:
            return render(request, 'statements/create.html', {'error':'All fields are required.'})
    else:
        return render(request, 'statements/create.html')


def detail(request, statement_id):
    statement = get_object_or_404(Statement, pk=statement_id)  #pk=primary key
    return render(request, 'statements/detail.html', {'statement':statement})  #statements/

    # try:
    #     statement = Statement.objects.get(pk=statement_id)
    # except Statement.DoesNotExist:
    #     raise Http404("Statement does not exist")
    # return render(request, 'statements/detail.html', {'statement':statement})

#    return HttpResponse("You're looking at question %s." % statement_id)

# def detail(request, statement_id):
#     statement = get_object_or_404(Statement, pk=statement_id)  #pk=primary key
#     return render(request, 'statements/detail.html', {'statement':statement})  #statements/
    

def results(request, statement_id):
    statement = get_object_or_404(Statement, pk=statement_id)
    numDisagree = Response.objects.filter(statement_id=statement_id).filter(disagree=1).count()
    numAgree = Response.objects.filter(statement_id=statement_id).filter(agree=1).count()
    return render(request, 'statements/results.html', {'statement': statement, 'numDisagree': numDisagree, 'numAgree': numAgree})  #statements/


@login_required(login_url="/accounts/signup")
def giveResponseDisagree(request, statement_id):
    if request.method == 'POST':   
        statement = get_object_or_404(Statement, pk=statement_id)
        response = Response()
        response.user = request.user
        response.statement = statement
        response.response_date = timezone.datetime.now()
        response.disagree = 1
        response.agree = 0
        response.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(statement.id,)))    

    # probabyl should put in error handling here...
    # try:
    #     selected_choice = statement.choice_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the question voting form.
    #     return render(request, 'statements/detail.html', {
    #         'statement': statement,
    #         'error_message': "You d   idn't select a choice.",
    #     })
    # else:


@login_required(login_url="/accounts/signup")
def giveResponseAgree(request, statement_id):
    if request.method == 'POST':   
        statement = get_object_or_404(Statement, pk=statement_id)
        response = Response()
        response.user = request.user
        response.statement = statement
        response.response_date = timezone.datetime.now()
        response.disagree = 0
        response.agree = 1
        response.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(statement.id,)))    


@login_required(login_url="/accounts/signup")
def results0(request, statement_id):
    statement = get_object_or_404(Statement, pk=statement_id)

    #Response.objects.filter(statement_id=2).filter(answer=0).count()

#@login_required(login_url="/accounts/signup")
# def upvote_home(request, statement_id):
#     if request.method == 'POST':        
#         statement = get_object_or_404(statement, pk=statement_id)
#         if request.user not in statement.voters.all():
#             print("not in ")
#             statement.votes_total += 1
#             statement.voters.add(request.user)
#             statement.save() # this save is what actually changes the database
#             return redirect('/statements/' + str(statement.id))
#         else:
#             print("it's already in")
#            # upvote(request, Statement_id)


# @login_required(login_url="/accounts/signup")
# def upvote(request, statement_id):
#     if request.method == 'POST':
#         print("regular upvote")
#         statement = get_object_or_404(statement, pk=statement_id)
#         statement.votes_total += 1
#         statement.voters.add(request.user)
#         statement.save() # this save is what actually changes the database
#         return redirect('/statements/' + str(statement.id))


def save_user_geolocation(request):
    if request.method == 'POST':
        latitude = request.POST['lat']
        longitude = request.POST['long']
        UserGeoLocation.create(
            user = request.user,
            latitude= latitude,
            longitude = longitude,
            )
        return HttpResponse('')


# def index(request):
#     latest_statement_list = Statement.objects.order_by('-pub_date')[:5]
# #    template = loader.get_template('statements/home.html')
#     context = {'latest_statement_list': latest_statement_list}
#     return render(request, 'statements/home.html', context)
#   #  output = ', '.join([q.statement_text for q in latest_statement_list])
#   #  return HttpResponse(output)


# class LookupView(FormView):
#     form_class = LookupForm

#     def get(self, request):
#         return render_to_response('gigs/lookup.html')

#     def form_valid(self, form):
#         # Get data
#         latitude = form.cleaned_data['latitude']
#         longitude = form.cleaned_data['longitude']

#         # Get today's date
#         now = timezone.now()

#         # Get next week's date
#         next_week = now + timezone.timedelta(weeks=1)

#         # Get Point
#         location = Point(longitude, latitude, srid=4326)

#         # Look up events
#         events = Event.objects.filter(datetime__gte=now).filter(datetime__lte=next_week).annotate(distance=Distance('venue__location', location)).order_by('distance')[0:5]

#         # Render the template
#         return render_to_response('gigs/lookupresults.html', {
#             'events': events
#             })