from django.urls import path
from expectations.views import RegistrationAPIView, GithubSignUpAuthView, LoginAPIView, GetExpectationListView, ManagingExpectations

app_name = "expectations"

urlpatterns = [
    path(
        "user-registration/",
        RegistrationAPIView.as_view(),
        name="user_registration",
    ),
    path(
        "github-sign-up-auth/",
        GithubSignUpAuthView.as_view(),
        name="github-sign-up-auth",
        ),
    path(
        "user-login/",
        LoginAPIView.as_view(),
        name="user-login",
    ),
    path(
        "get-expectations-list/",
        GetExpectationListView.as_view(),
        name="get-expectations_list",
    ),
    path(
        "managing-expectations/",
        ManagingExpectations.as_view(),
        name="create_managing_expectations",
    ),
    path(
        "managing-expectations/<int:pk>/",
        ManagingExpectations.as_view(),
        name="update_or_delete_managing_expectations",
        )

]
