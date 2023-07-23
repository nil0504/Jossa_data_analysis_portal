from django.contrib import admin
from django.urls import path
from JOSSA import views
from .views import authentication,courses,analysis,top

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication().signup, name='sign-up'),
    path('login/', authentication().login, name='login'),
    path('home/',analysis().home, name='home'),
    path('branche/', analysis().branche, name='branche'),
    path('institute/', analysis().institute, name='institute'),
    path('course_probablity/', analysis().course_probablity, name='course_probablity'),
    path('btech/', courses().btech, name='btech'),
    path('mtech/', courses().mtech, name='mtech'),
    path('other/', courses().other, name='other'),
    path('top_courses/', top().top_courses, name='top_courses'),
    path('top_iit/', top().top_iits, name='top_iit'),
    path('login2/', views.login2, name='login2'), # for input data in database
    ]

