from django.urls import path
from rest_framework.routers import SimpleRouter

from habits.apps import HabitsConfig
from habits.views import HabitsViewSet

app_name = HabitsConfig.name

router = SimpleRouter()
router.register('', HabitsViewSet, basename='habits')


urlpatterns = []

urlpatterns += router.urls
