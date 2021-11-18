from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import Http404
from django.urls.base import reverse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    View,
    UpdateView,
    FormView,
    DeleteView,
)
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from users import mixins as user_mixins
from . import models, forms


# 함수 방식은 여러게 많은 기능들을 담당할때 사용하면 좋고
# class view 방식은 하나의 목적을 가진 기능을 작업할때 사용하면 용이하다

# 클레스뷰는 매직하게 돌아간다
# 하지만 장고 도큐먼트에서 요소를 찾아야 알맞는 설정을 세팅할 수 있는데
# 다행이도 https://ccbv.co.uk/projects/Django/2.2/ 에서 요소와 관련해 정리해 두었다.


class HomeView(ListView):
    """HomeView Definition"""

    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


class RoomDetail(DetailView):
    """RoomDetail Definition"""

    model = models.Room


class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "어디든지":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")
                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


# 만약 country에 아무것도 안들어있거나 오류가 있다면 빈 form을 생성하고 form을 렌더하고 끝낸다.
# 문제가 없다면 if form.is_valid()에서 작성한 코드가 잘 작동될것이다.
# 결국 했던것은 유저가 url을 건들여서 망칠것을 대비하고, 처음 빈 서치 폼으로 돌아왔을때 초기 화면을 만들어준것이다.
class DeleteRoomView(user_mixins.LoggedInOnlyView, DeleteView, SuccessMessageMixin):
    model = models.Room
    context_object_name = "target_team"
    success_url = reverse_lazy("core:home")
    success_message = "방 삭제 완료!"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "gusests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "사진을 삭제할 수 없습니다.")
        else:

            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "사진을 삭제했습니다.")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))

    except models.Room.DoesNotExist:
        return redirect(reverse("core:home "))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Updated"
    fields = ("caption",)

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        form.save_m2m()
        messages.success(self.request, "Room Created")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
