from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from .forms import *
urlpatterns = [
    path('', views.home),
    path('product-detail/', views.product_detail, name='product-detail'),
    path('cart/', views.add_to_cart, name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',
    form_class=ChangePasswordForm, success_url='/passwordchangedone/'), name='changepassword'),
    
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),
    name='passwordchangedone'),
    
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', 
    form_class=MyPasswordResetForm),name='password-reset'),

    path('password-reset-done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'
    ),name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view
    (template_name='app/password_reset_confirm.html', form_class=MySetPasswordResetForm),name='password_reset_confirm'),

    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view
    (template_name='app/password_reset_complete.html'),name='password_reset_complete'),

    path('mobile/', views.mobile, name='mobile'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', 
    authentication_form=LoginForm), name='login'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('checkout/', views.checkout, name='checkout'),
]
