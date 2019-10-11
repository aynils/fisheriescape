from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name="index"),

    # EVENT #
    ##########
    path('trips/', views.EventListView.as_view(), name="event_list"),
    path('trip/new/', views.EventCreateView.as_view(), name="event_new"),
    path('trip/<int:pk>/view/', views.EventDetailView.as_view(), name="event_detail"),
    path('trip/<int:pk>/print/', views.TravelPlanPDF.as_view(), name="event_print"),
    path('trip/<int:pk>/edit/', views.EventUpdateView.as_view(), name="event_edit"),
    path('trip/<int:pk>/delete/', views.EventDeleteView.as_view(), name="event_delete"),
    path('trip/<int:pk>/duplicate/', views.duplicate_event, name="duplicate_event"),

    # Reports #
    ###########
    path('reports/search/', views.ReportSearchFormView.as_view(), name="report_search"),
    path('reports/export-cfts-list/<int:fy>/', views.export_cfts_list, name="export_cfts_list"),
    # path('event/<int:fy>/<str:email>/print/', views.TravelPlanPDF.as_view(), name="travel_plan"),



]
