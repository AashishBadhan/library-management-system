from rest_framework import viewsets
from django.contrib.auth import get_user_model
from api.serializers import UserSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@login_required
def profile_view(request):
    """Display and update the authenticated user's profile (CustomUser fields)."""
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.address = request.POST.get('address', user.address)
        if 'avatar' in request.FILES:
            user.profile_picture = request.FILES['avatar']
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('user_profile')
    return render(request, 'profile.html', {'user_obj': user})
