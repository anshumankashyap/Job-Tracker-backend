from django.urls import path
from .views import AnalyzeResumeView

urlpatterns = [
    path('<int:pk>/analyze/', AnalyzeResumeView.as_view(), name='analyze-resume'),
]