from django.urls import path
from . import views

app_name = "rooms"
urlpatterns = [
    path("create/", views.CreateRoomView.as_view(), name="create"),
    path("<int:pk>/", views.RoomDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.DeleteRoomView.as_view(), name="delete"),
    path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),
    path("<int:pk>/photos/add/", views.AddPhotoView.as_view(), name="add-photo"),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/delete/",
        views.delete_photo,
        name="delete-photo",
    ),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/edit/",
        views.EditPhotoView.as_view(),
        name="edit-photo",
    ),
    path("search/", views.SearchView.as_view(), name="search"),
]
# views 페이지에서 RoomDetail를 클레스 베이스 뷰 방식으로 사용할때 DeleteView를 상속받았다.
# DeleteView가 우리의 디테일 페이지의 모델을 알수있었던 이유는 기본적으로 DeleteView는 pk 받도록 되어있는데
# 우리의 urls 페이지에서 장고가 확인하고 넘겨주기 때문
# 이름이 꼭 pk가 아니더라도 저번에 사용했던 클레스 요소 확인 사이트에서 pk라는 이름대신 banana 처럼 자유롭게 가능
