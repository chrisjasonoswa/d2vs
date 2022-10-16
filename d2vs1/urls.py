from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("index", views.index, name="index"),
]

htmx_urlpatterns =[
    path("home", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),

    path("update-username", views.update_username, name="update_username"),
    path("update-password", views.update_password, name="update_password"),
    path("update-dashboard", views.update_dashboard, name="update_dashboard"),
    path("update-phonenumber", views.update_phonenumber, name="update_phonenumber"),

    path("register-knock", views.register_knock, name="register_knock"),

    path("add-logs", views.add_logs_get, name="add_logs_get"),
    path("add-logs/<str:status>/<int:user_id>", views.add_logs, name="add_logs"),

    path("get-logs", views.get_logs, name="get_logs"),
    path("get-recent-logs", views.get_recent_logs, name="get_recent_logs"),

    path("clear-logs", views.clear_logs, name="clear_logs"),

    path("controls", views.controls, name="controls"),
    path("system-status", views.update_system_status, name="update_system_status"),
    path("current-system-status", views.get_current_status, name="get_current_status"),
    path("manual-control", views.manual_control, name="manual_control"),
    path("set_password", views.set_password, name="set_password"),
    path("del_password/<str:key>", views.del_password, name="del_password"),
    path("logs", views.logs, name="logs"),
]

urlpatterns += htmx_urlpatterns