from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Statement
from django.utils import timezone

from django.views.generic.edit import FormView
from statements.forms import LookupForm
#from django.shortcuts import render_to_response

def home(request):
    statements = Statement.objects.all().order_by('-votes_total') # gets all the projects out of the database
    return render(request, 'statements/home.html', {'statements':statements})

@login_required(login_url="/accounts/signup")
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and \
            request.POST['url'] and request.FILES['image'] and request.FILES['icon']:
            Statement = Statement()
            Statement.title = request.POST['title']
            Statement.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                Statement.url = request.POST['url']
            else:
                Statement.url = 'http://' + request.POST['url']
            Statement.image = request.FILES['image']
            Statement.icon = request.FILES['icon']            
            Statement.pub_date = timezone.datetime.now()
            #Statement.votes_total = 1
            Statement.hunter = request.user
            Statement.save() # inserts it into the database
            return redirect('/statements/' + str(Statement.id)) # show user the Statement
        else:
            return render(request, 'statements/create.html', {'error':'All fields are required.'})
    else:
        return render(request, 'statements/create.html')

def detail(request, Statement_id):
    Statement = get_object_or_404(Statement, pk=Statement_id)  #pk=primary key
    return render(request, 'statements/detail.html', {'Statement':Statement})

@login_required(login_url="/accounts/signup")
def upvote_home(request, Statement_id):
    if request.method == 'POST':        
        Statement = get_object_or_404(Statement, pk=Statement_id)
        if request.user not in Statement.voters.all():
            print("not in ")
            Statement.votes_total += 1
            Statement.voters.add(request.user)
            Statement.save() # this save is what actually changes the database
            return redirect('/statements/' + str(Statement.id))
        else:
            print("it's already in")
           # upvote(request, Statement_id)


@login_required(login_url="/accounts/signup")
def upvote(request, Statement_id):
    if request.method == 'POST':
        print("regular upvote")
        Statement = get_object_or_404(Statement, pk=Statement_id)
        Statement.votes_total += 1
        Statement.voters.add(request.user)
        Statement.save() # this save is what actually changes the database
        return redirect('/statements/' + str(Statement.id))


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