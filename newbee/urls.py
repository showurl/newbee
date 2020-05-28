from django.urls import path
from newbee import views as newbee_view
from newbee.config import PATH

urlpatterns = [
    path(PATH, newbee_view.NewBeeView.as_view()),
]