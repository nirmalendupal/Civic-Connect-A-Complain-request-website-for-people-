from django.contrib import admin
from django.urls import path, re_path
from problems import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('problem/<int:pk>/', views.problem_detail, name='problem_detail'),

    # Naye Public Login/Signup ke URLs
    path('signup/', views.signup_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
]

# Serve user-uploaded photos (problem report images) at all times, not just
# when DEBUG=True. Django's static() helper is a no-op whenever DEBUG=False
# (that's a hard-coded safety check inside static() itself, regardless of
# where you call it from) — so we call the underlying view directly instead.
# Whitenoise's middleware handles STATIC files in production, but it does NOT
# serve MEDIA files (they're uploaded at runtime, not collected at build
# time), so without this every uploaded image 404s in production. This is
# fine for a small/demo app serving media straight from disk; for a bigger
# production app you'd typically use a dedicated object storage service
# (e.g. S3) instead.
urlpatterns += [
    re_path(
        r'^media/(?P<path>.*)$',
        static_serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=str(settings.BASE_DIR / 'static'))