from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib import messages
from .models import User, Donner, LikePost, Message, Division, Location, Contact, BloodInfoAddProblem, Management
from .forms import PersonCreationForm, ContactForm, BiapForm, MyUserCreationForm, EditProfile, UserUploadDonerUpdareForm
from .filters import BloodFilter
from datetime import date
from django.db.models import Count


# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    blood_donner = Donner.objects.filter(
        Q(name__icontains=q) |
        Q(phone__icontains=q)
    )
    
    blood_filter = BloodFilter(request.GET, queryset=blood_donner)
    return render(request, 'home.html', {'blood_filter':blood_filter })


def Profile(request, username):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    try:
        user_object = User.objects.get(username=username)
        upost = user_object.donner_set.all()
        userpost = user_object.donner_set.filter(
            Q(name__icontains=q) |
            Q(phone__icontains=q)
        )
        countpost = upost.count()

    except User.DoesNotExist:
        return HttpResponse("Something went wrong.")        

    context = {'user_object':user_object, 'userpost':userpost, 'countpost':countpost}
    return render(request, "profile.html", context)


@login_required(login_url='login')
def updateUser(request, username):
    user = request.user
    user_form = EditProfile(instance=user)

    if request.method == 'POST':
        user_form = EditProfile(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect('update-profile', username=user.username)

    return render(request, 'update-profile.html', {'user_form':user_form})


def donner(request, pk):
    donner = Donner.objects.get(id=pk)
    messages = donner.message_set.all()
    
    today = date.today()
    d_date = donner.donation_date
    if d_date == None:
        donate_time = 121
    else:
        donate_time = today - d_date
        donate_time = donate_time.days

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            donner=donner,
            body=request.POST.get('body')
        )
        return redirect('donner', pk=donner.id)

    context = {'donner': donner, 'messages': messages, 'donate_time':donate_time}
    return render(request, 'single.html', context)


#like post function
@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')


def blood_create_view(request):
    form = PersonCreationForm()
    if request.method == 'POST':
        form = PersonCreationForm(request.POST)
        if form.is_valid():
            try:
                form = form.save(commit=False)
                form.author = request.user
                form.save()
            except:
                form.save()
            messages.info(request, 'আপনার তথ্য প্রদান সফল হয়েছে। আপনাকে অসংখ্য ধন্যবাদ। ')
            return redirect('blood-info-add')
        else:
            messages.info(request, "আপনার প্রদানকৃত মোবাইল নম্বরটি ভুল অথবা মোবাইল নম্বরটি একবার ব্যবহার করা হয়েছে। দয়া করে ১১ ডিজিটের মোবাইল নম্বর দিন অথবা মোবাইল নম্বর পরিবর্তন করুন। ")
    return render(request, 'upload.html', {'form': form})


def updateBloodInfo(request, pk):
    donner = Donner.objects.get(id=pk)
    form = PersonCreationForm(instance=donner)

    if request.method == 'POST':
        donner.donation_date = request.POST.get('donation_date')
        donner.save()
        return redirect('donner', pk=donner.id)

    context = {'form': form, 'donner': donner}
    return render(request, 'update.html', context)


# User uploaded Donner info update 
@login_required(login_url='login')
def userBloodInfo(request, pk):
    donner = Donner.objects.get(id=pk)
    ub_form = UserUploadDonerUpdareForm(instance=donner)
    user = Donner.objects.get(id=pk)

    if request.method == 'POST':
        ub_form = UserUploadDonerUpdareForm(request.POST, instance=donner)
        if ub_form.is_valid():
            ub_form.save()
            #messages.info(request, 'Successfully update donner info.')
            return redirect('profile', donner.author.username)

    return render(request, 'user-update.html', {'ub_form':ub_form, 'donner':donner})


def RegisterUser(request):
    regi_form = MyUserCreationForm()

    if request.method == 'POST':
        regi_form = MyUserCreationForm(request.POST)
        if regi_form.is_valid():
            user = regi_form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            name = regi_form.cleaned_data.get('name')
            messages.success(request, f"New Account Created: {name}")
            login(request, user)
            messages.info(request, f"You are now logged in as {name}")
            return redirect('home')
        else:
          # for msg in form.error_messages:
          #   messages.error(request, f"{msg}: {form.error_messages[msg]}")
          #   print(msg)
            password1 = regi_form.data['password1']
            password2 = regi_form.data['password2']
            email = regi_form.data['email']
            username = regi_form.data['username']
             
            for msg in regi_form.errors.as_data():
                if msg == 'email':
                    messages.error(request, f"Declared {email} is not valid")
                elif msg == 'username':
                    messages.error(request, f"Declared {username} is not valid")
                elif msg == 'password2' and password1 == password2:
                    messages.error(request, f"Selected password: {password1} is not strong enough")
                elif msg == 'password2' and password1 != password2:
                    messages.error(request, "The two password fields didn’t match.")

    return render(request, 'register.html', {'regi_form': regi_form})


#Log-in User
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    return render(request, 'login.html')


#Log-out
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')


def Contact(request):
    cnt_form = ContactForm()
    if request.method == 'POST':
        cnt_form = ContactForm(request.POST)
        if cnt_form.is_valid():
            cnt_form.save()
            messages.info(request, 'Thanks for contact us. We will response within a short time.')
            return redirect('contact-us')
        else:
            messages.info(request, "There was a problem while submiting contact form")
    return render(request, 'contact.html', {'cnt_form': cnt_form})


# Management Body
def management(request):
    magmnt = Management.objects.all()
    
    return render(request, 'management.html', {'magmnt':magmnt})



def BloodInfoAddProblem(request):
    biap_form = BiapForm()
    if request.method == 'POST':
        biap_form = BiapForm(request.POST)
        if biap_form.is_valid():
            biap_form.save()
            messages.info(request, 'Thanks for contact us. We will response within a short time.')
            return redirect('blood-info-add')
        else:
            messages.info(request, "There was a problem while submiting contact form")
    return render(request, 'contact.html', {'biap_form': biap_form})


# Page not found
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


@property
def image_url(self):
    if self.image and hasattr(self.image, 'url'):
        return self.image.url


# AJAX
def load_cities(request):
    division_id = request.GET.get('division_id')
    locations = Location.objects.filter(division_id=division_id).all()
    return render(request, 'city_dropdown_list_options.html', {'locations': locations})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)

































