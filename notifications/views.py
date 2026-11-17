from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Notification
from django.shortcuts import redirect

from django.http import JsonResponse


@login_required
def notification_list(request):

    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)

    notifications = Notification.objects.filter(
        user=request.user
    )

    return render(
        request,
        "notifications/notification_list.html",
        {
            "notifications": notifications
        }
    )
@login_required
def mark_all_read(request):

    Notification.objects.filter(

        user=request.user,

        is_read=False

    ).update(is_read=True)

    return redirect("notifications")

@login_required
def notification_api(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")[:5]

    data=[]

    for n in notifications:

     data.append({
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "type": n.notification_type,
            "created_at": n.created_at.strftime("%d %b %Y %I:%M %p"),
      })

    unread=Notification.objects.filter(

        user=request.user,

        is_read=False

    ).count()

    return JsonResponse({

        "notifications":data,

        "unread_count":unread

    })