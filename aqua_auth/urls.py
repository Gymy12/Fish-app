from django.urls import path
from . import views

urlpatterns = [
    path("login", views.signin, name="signin"),
    path("register", views.signup, name="signup"),
    path("logout", views.signout, name="signout"),
    # path("forgot-password", views.forgot_password, name="forgot_password"),
    # path("reset-password", views.reset_password, name="reset_password"),
    path("profile", views.profile, name="profile"),
    path("change-password", views.change_password, name="change-password"),
    path("update-profile", views.update_profile, name="update-profile"),
    # path("delete-account", views.delete_account, name="delete_account"),
]
