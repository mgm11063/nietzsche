from django.contrib import messages
from django.shortcuts import redirect
from django.urls.base import reverse
from rooms import models as room_models
from . import forms


def create_review(request, room):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room)
        if not room:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, "room reviewed")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
        else:
            messages.error(request, "It's Not Valid Form")
            return redirect(reverse("core:home"))
