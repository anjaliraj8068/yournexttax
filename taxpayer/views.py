from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Taxpayer
from .forms import TaxpayerForm


@login_required
def profile(request):

    taxpayer = Taxpayer.objects.filter(user=request.user).first()

    if request.method == "POST":

        if taxpayer:

            form = TaxpayerForm(request.POST, instance=taxpayer)

        else:

            form = TaxpayerForm(request.POST)

        if form.is_valid():

            if "profile_image" in request.FILES:
                request.user.profile_image = request.FILES["profile_image"]
                request.user.save()

            profile = form.save(commit=False)

            profile.user = request.user

            profile.save()

            messages.success(request, "Profile saved successfully.")

            return redirect("profile")

    else:

        if taxpayer:

            form = TaxpayerForm(instance=taxpayer)

        else:

            form = TaxpayerForm()

    return render(
        request,
        "taxpayer/profile.html",
        {"form": form}
    )