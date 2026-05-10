from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.




def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful 🎉")
            return redirect('home')  # change if needed
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')



from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Session update — logout na ho user
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'profile.html', {'form': form})


# ===========================
# PASSWORD CHANGE
# ===========================
@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'profile.html', {'form': form})





def user_logout(request):
    logout(request)   # clears session
    messages.success(request, "You have been logged out 👋")
    return redirect('home')
    
