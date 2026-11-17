from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.ai_recommendation_loading,
        name="ai_recommendation"
    ),

    path(
        "generate/",
        views.process_ai_recommendation,
        name="process_ai_recommendation"
    ),

    path(
        "history/",
        views.report_history,
        name="report_history"
    ),

    path(
        "download/<int:pk>/",
        views.download_report,
        name="download_report"
    ),

    # Chat UI
    path(
        "chatbot/",
        views.chatbot,
        name="chatbot"
    ),

    # AJAX API
    path(
        "chat/",
        views.chatbot_api,
        name="chatbot_api"
    ),

]