from .models import Notification


def generate_notifications(user, income, deduction):

    Notification.objects.filter(user=user).delete()

    if deduction < 150000:

        Notification.objects.create(
            user=user,
            title="Section 80C",
            message="Section 80C limit not completed.",
            notification_type="warning"
        )

    Notification.objects.create(
        user=user,
        title="ITR Reminder",
        message="ITR filing date is approaching.",
        notification_type="info"
    )

    Notification.objects.create(
        user=user,
        title="Health Insurance",
        message="Add Health Insurance under Section 80D.",
        notification_type="success"
    )

    Notification.objects.create(
        user=user,
        title="NPS",
        message="NPS investment recommended.",
        notification_type="primary"
    )

from .models import Notification


def create_notification(
    user,
    title,
    message,
    notification_type="info"
):

    Notification.objects.create(

        user=user,

        title=title,

        message=message,

        notification_type=notification_type

    )