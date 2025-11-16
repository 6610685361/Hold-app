from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from RandomFood.models import Food


@staff_member_required
def admin_dashboard(request):
    # Top 10 foods with highest favorite count
    top_foods = Food.objects.order_by("-favorite_count")[:10]

    return render(
        request,
        "pages/admin_dashboard.html",
        {
            "top_foods": top_foods,
        },
    )


def home(request):
    return render(request, "pages/home.html")


def about(request):
    return render(request, "pages/AboutUs.html")
