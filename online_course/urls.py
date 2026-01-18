from django.urls import path
from . import views

app_name = 'online_course'
urlpatterns = [
    path('<int:course_id>/submit/', views.submit, name='submit'),
    path('<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='submission_result'),
]
