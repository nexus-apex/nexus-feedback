from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('feedbackitems/', views.feedbackitem_list, name='feedbackitem_list'),
    path('feedbackitems/create/', views.feedbackitem_create, name='feedbackitem_create'),
    path('feedbackitems/<int:pk>/edit/', views.feedbackitem_edit, name='feedbackitem_edit'),
    path('feedbackitems/<int:pk>/delete/', views.feedbackitem_delete, name='feedbackitem_delete'),
    path('feedbackcategories/', views.feedbackcategory_list, name='feedbackcategory_list'),
    path('feedbackcategories/create/', views.feedbackcategory_create, name='feedbackcategory_create'),
    path('feedbackcategories/<int:pk>/edit/', views.feedbackcategory_edit, name='feedbackcategory_edit'),
    path('feedbackcategories/<int:pk>/delete/', views.feedbackcategory_delete, name='feedbackcategory_delete'),
    path('fbresponses/', views.fbresponse_list, name='fbresponse_list'),
    path('fbresponses/create/', views.fbresponse_create, name='fbresponse_create'),
    path('fbresponses/<int:pk>/edit/', views.fbresponse_edit, name='fbresponse_edit'),
    path('fbresponses/<int:pk>/delete/', views.fbresponse_delete, name='fbresponse_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
