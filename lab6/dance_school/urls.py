from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.template.defaulttags import url
from django.urls import path, include, re_path

from dance_school.views import ChoreographersListView, ChoreoDetailView, ChoreoCreateView, ChoreoUpdateView, \
    ChoreoStyleUpdateView, GroupDanceListView, GroupDetailView, DancerDetailView, DancerCreateView, DancerUpdateView, \
    ScheduleCreateView, DancerVisitView

urlpatterns = [
    path('choreo/', ChoreographersListView.as_view(), name='choreo_list'),
    path('choreo/info/<int:pk>/', ChoreoDetailView.as_view(), name='choreo_detail'),
    path('choreo/styles/<int:pk>/', ChoreoStyleUpdateView.as_view(), name='choreo_style'),
    path('groups/', GroupDanceListView.as_view(), name='group_list'),
    path('group/<int:pk>/', GroupDetailView.as_view(), name='group_detail'),
    path('dancer/add/', DancerCreateView.as_view(), name='dancer_add'),
    path('dancer/update/<int:pk>/', DancerUpdateView.as_view(), name='dancer_update'),
    path('choreo/add/', ChoreoCreateView.as_view(), name='choreo_add'),
    path('choreo/update/<int:pk>/', ChoreoUpdateView.as_view(), name='choreo_update'),
    path('dancer/info/<int:pk>/', DancerDetailView.as_view(), name='dancer_detail'),
    path('addshedule/', ScheduleCreateView.as_view(), name='add_schedule'),
    path('addshedule/<int:group_id>/<int:lesson_id>', DancerVisitView.as_view(), name='dancer_visit')
]
