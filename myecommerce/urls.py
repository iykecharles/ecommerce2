"""myecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import register, profile
from django.contrib.auth.views import LoginView, LogoutView
from market.views import MarketListView, MarketDetailView, MarketCreateView, MarketUpdateView, MarketDeleteView, ProductListView, OrderSummaryView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from market.views import add_to_cart, remove_from_cart, remove_single_item_cart, CheckoutView, Payment

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('register/', register, name="register"),
    path('profile/', profile, name="profile"),
    path('login/', LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path('password-reset/', PasswordResetView.as_view(template_name="users/password-reset.html"), name="password-reset"),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name="users/password-reset-done.html"), name="password-reset-done"),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), name="password_reset_confirm"),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name="password_reset_complete"),
    path('', MarketListView.as_view(), name="market"),
    path('product/', ProductListView.as_view(), name="product"),
    path('market/<int:pk>/', MarketDetailView.as_view(), name="market-details"),
    path('market/create/', MarketCreateView.as_view(), name="market-create"),
    path('order-summary/', OrderSummaryView.as_view(), name="order-summary"),
    path('add_to_cart/<int:pk>/', add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:pk>/', remove_from_cart, name="remove_from_cart"),
    path('remove_single_item_cart/<int:pk>/', remove_single_item_cart, name="remove_single_item_cart"),
    path('checkoutView/',
         CheckoutView.as_view(), name="checkoutView"),
    path('payment/<payment_type>/', Payment.as_view(), name="payment"),
    



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
