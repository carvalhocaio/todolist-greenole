from rest_framework import routers

from todo import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"todos", views.ToDoViewSet)

urlpatterns = router.urls
