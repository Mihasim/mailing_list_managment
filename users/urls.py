from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, ClientDeleteView, \
    RegisterView, UserConfirmEmailView, EmailConfirmationSentView, FailedView, EmailConfirmedView, UserFormView, \
    UserListView, UserDetailView, UserUpdateView, UserDeleteView

app_name = UsersConfig.name

urlpatterns = [
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('client_detail<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('client/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/verify_send/', EmailConfirmationSentView.as_view(), name='verify_send'),
    path('profile/error_page/', FailedView.as_view(), name='error_page'),
    path('profile/email_verified/', EmailConfirmedView.as_view(), name='email_verified'),
    path('profile/email_verified/<str:verification_code>/', UserConfirmEmailView.as_view(), name='email_verified'),
    path('user_form/', UserFormView.as_view(), name='user_form'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('user_detail<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('user/<int:pk>', UserDeleteView.as_view(), name='user_delete'),
]
