from datetime import datetime
from django.contrib import messages
from django.utils.timezone import now
from django.shortcuts import redirect, render
from events.forms import EventModelForm,CategoryModelForm, ParticipantModelForm
from events.models import Participant, Event, Category


def organizer_dashboard(request):
    today = now().date()

    # Base queryset
    base_query = Event.objects.select_related('category').prefetch_related('participant_set')

    # Statistics (Optional Summary Counts)
    counts = {
        'total_events': base_query.count(),
        'total_participants': Participant.objects.count(),
        'today_events': base_query.filter(date__date=today).count(),
        'upcoming_events': base_query.filter(date__date__gt=today).count(),
        'past_events': base_query.filter(date__date__lt=today).count(),
    }

    # Filtering by type (from query param)
    type = request.GET.get('type', 'all').lower()

    if type == 'today':
        events = base_query.filter(date__date=today)
    elif type == 'upcoming':
        events = base_query.filter(date__date__gt=today)
    elif type == 'past':
        events = base_query.filter(date__date__lt=today)
    else:
        events = base_query.all()
    
    print(events)
    context = {
        'events': events,
        'counts': counts,
        'type': type,
    }

    return render(request, 'organize_dashboard.html', context)


def view_events(request):
    id = request.GET.get('type')
    print(id)
    event= Event.objects.select_related('category').prefetch_related('participant_set').get(id=id)
    context = {
        'event': event,
    }
    return render(request, 'view_events.html',context)



def create_event(request):
    event = EventModelForm()    
    category = CategoryModelForm()
    participant = ParticipantModelForm()

    context = {'event_form': event,'category_form': category, 'participant_form': participant}
    # context = {'event_form': event}

    if request.method == 'POST':
        event = EventModelForm(request.POST)
        category = CategoryModelForm(request.POST)
        participant = ParticipantModelForm(request.POST)
        
    if event.is_valid() and category.is_valid() and participant.is_valid():
        # Save category
        category_obj = category.save()  
        category_obj = category.instance  

        # Save event
        event_obj = event.save(commit=False)
        event_obj.category = category_obj
        event_obj.save()

        # Save participant
        participant_obj = participant.save(commit=False)
        participant_obj.save()
        participant_obj.events.add(event_obj)


    return render(request, 'event_form.html',context)




def edit_event(request,id):
    event_instance = Event.objects.get(id=id)
    event = EventModelForm(instance=event_instance)    
    category = CategoryModelForm(instance=event_instance.category)
    participant = ParticipantModelForm(instance=event_instance.participant_set.first())

    context = {'event_form': event,'category_form': category, 'participant_form': participant}
    # context = {'event_form': event}

    if request.method == 'POST':
        event = EventModelForm(request.POST)
        category = CategoryModelForm(request.POST)
        participant = ParticipantModelForm(request.POST)
        
    if event.is_valid() and category.is_valid() and participant.is_valid():
        # Save category
        category_obj = category.save()  
        category_obj = category.instance  

        # Save event
        event_obj = event.save(commit=False)
        event_obj.category = category_obj
        event_obj.save()

        # Save participant
        participant_obj = participant.save(commit=False)
        participant_obj.save()
        participant_obj.events.add(event_obj)


    return render(request, 'dashboard.html',context)



def delete_event(request, id):    
    if request.method == 'POST':
        event_instance = Event.objects.get(id=id)
        event_instance.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('organizer_dashboard')
        