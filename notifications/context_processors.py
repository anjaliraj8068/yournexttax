from .models import Notification


def notification_context(request):

    if request.user.is_authenticated:

        latest = Notification.objects.filter(
            user=request.user
        ).order_by("-created_at")[:5]

        unread = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

        return {

            "latest_notifications": latest,

            "unread_notifications": unread,

        }

    return {}