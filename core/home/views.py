from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from .models import Event
from datetime import timedelta
from django.views.decorators.http import require_POST

def create_event(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        hours = request.POST.get("hours", "0").strip()
        minutes = request.POST.get("minutes", "0").strip()
        seconds = request.POST.get("seconds", "0").strip()

        if not name:
            messages.error(request, "Please enter event name.")
            return render(request, "create_event.html")

        try:
            h = int(hours)
            m = int(minutes)
            s = int(seconds)
        except ValueError:
            messages.error(request, "Hours, minutes and seconds must be integer numbers.")
            return render(request, "create_event.html")

        if h < 0 or m < 0 or s < 0:
            messages.error(request, "Hours, minutes and seconds must be >= 0.")
            return render(request, "create_event.html")

        total_seconds = h * 3600 + m * 60 + s
        if total_seconds <= 0:
            messages.error(request, "Duration must be greater than 0.")
            return render(request, "create_event.html")

        event_date = timezone.now() + timedelta(seconds=total_seconds)

        event = Event.objects.create(
            name=name,
            event_date=event_date,
            remaining_seconds=None,
            status=Event.STATUS_RUNNING
        )
        return redirect("event_detail", uid=event.uid)

    return render(request, "create_event.html")


def event_detail(request, uid):
    event = get_object_or_404(Event, uid=uid)
    return render(request, "event_detail.html", {
        "event": event,
    })


def events_list(request):
    events = Event.objects.all().order_by('-created_at')
    return render(request, "events_list.html", {"events": events})


@require_POST
def pause_event(request, uid):
    event = get_object_or_404(Event, uid=uid)
    now = timezone.now()

    if event.status == Event.STATUS_PAUSED and event.remaining_seconds is not None:
        return JsonResponse({"status": "ok", "remaining_seconds": event.remaining_seconds, "message": "Already paused"})

    remaining = (event.event_date - now).total_seconds()
    if remaining <= 0:
        event.status = Event.STATUS_FINISHED
        event.remaining_seconds = 0
        event.save()
        return JsonResponse({"status": "finished", "message": "Event already finished."})

    event.remaining_seconds = int(remaining)
    event.status = Event.STATUS_PAUSED
    event.save()
    return JsonResponse({"status": "ok", "remaining_seconds": event.remaining_seconds})


@require_POST
def resume_event(request, uid):
    event = get_object_or_404(Event, uid=uid)
    now = timezone.now()

    if event.status != Event.STATUS_PAUSED or event.remaining_seconds is None:
        return JsonResponse({"status": "error", "message": "Event is not paused."}, status=400)

    event.event_date = now + timedelta(seconds=int(event.remaining_seconds))
    event.remaining_seconds = None
    event.status = Event.STATUS_RUNNING
    event.save()
    return JsonResponse({"status": "ok", "event_date_iso": event.event_date.isoformat()})


@require_POST
def delete_event(request, uid):
    event = get_object_or_404(Event, uid=uid)
    event.delete()
    return JsonResponse({"status": "ok", "message": "Event deleted."})

def events_list(request):
    events = Event.objects.all().order_by('-created_at')
    return render(request, 'events_list.html', {
        'events': events
    })

