from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import RegisterUserForm, UserEditForm, ProfileEditForm, CreateProfileForm
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from .forms import UploadFileForm
from .admin import UserResource
from tablib import Dataset
from import_export.formats import base_formats
from django.views.generic import FormView
from django.urls import reverse_lazy
from import_export.admin import ImportExportModelAdmin
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.success(request, ("Tên đăng nhập hoặc mật khẩu không đúng, Vui lòng thử lại"))
                return redirect('login')
    return render(request, 'authentication/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,("Đăng ký thành công"))
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request, 'authentication/register.html', {'form':form})

class UserListView(ListView):
    # model = User
    queryset = User.objects.all().filter(is_superuser=0)
    template_name = 'authentication/member.html'
    context_object_name = 'Users'
    paginate_by = 7
    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['nu'] = Profile.objects.filter(gioitinh='Nữ')
        context['nam'] = Profile.objects.filter(gioitinh='Nam').exclude(user=1)
        context['tongnhanvien'] = User.objects.all().filter(is_superuser=0)
        context['2020'] = Profile.objects.all().filter(ngayvaocty__year=2020).exclude(user=1)
        context['2021'] = Profile.objects.all().filter(ngayvaocty__year=2021).exclude(user=1)
        context['2022'] = Profile.objects.all().filter(ngayvaocty__year=2022).exclude(user=1)
        context['2023'] = Profile.objects.all().filter(ngayvaocty__year=2023).exclude(user=1)
        return context

def search_venues(request):
    if request.method == "POST":
        searched=request.POST['searched']

        venues = User.objects.filter(is_superuser=0).filter(Q(username__contains=searched) | Q(last_name__contains=searched) | Q(first_name__contains=searched))
        return render(request,'authentication/search-venues.html',{'searched':searched, 'venues':venues})
    else:
        return render(request,'authentication/search-venues.html',{})

# @login_required
def edit_user(request):
    user_form = RegisterUserForm()
    if request.method == 'POST':
        user_form = RegisterUserForm(instance=request.user,data=request.POST)
        # profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES,user=request.user,msnv='298',hovaten='Mai Thuc Trinh', phongban=1,chucdanh='Nhan vien',gioitinh='Nu',ngaysinh='2020-01-30',)
        if user_form.is_valid():
            user_form.save()
            # profile_form.save()
        return redirect('edit')
    else:
        user_form = RegisterUserForm(instance=request.user)
        # profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'authentication/edit.html',{'user_form': user_form})

def CreateProfile(request):
    # post = get_object_or_404(Post, pk=pk)
    form = CreateProfileForm()
    if request.method =='POST':
        form = CreateProfileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            # post = form.save(commit=False)
            form.save()
            # comment = Comment.objects.create(post=form, author=request.user, body='')
        return HttpResponseRedirect(reverse('createprofile'))
    return render(request, "authentication/profilecreation.html", {"form":form})

def EditProfile(request):
    # post = get_object_or_404(Post, pk=pk)
    form = CreateProfileForm()
    if request.method =='POST':
        form = CreateProfileForm(instance=request.user.profile,data=request.POST,files=request.FILES, user=request.user)
        if form.is_valid():
            # post = form.save(commit=False)
            form.save()
            # comment = Comment.objects.create(post=form, author=request.user, body='')
        return HttpResponseRedirect(reverse('editprofile'))
    else:
        form = CreateProfileForm(instance=request.user.profile)
    return render(request, "authentication/editprofile.html", {"form":form})

def EditProfileAll(request,pk):
    # post = get_object_or_404(Post, pk=pk)
    user = get_object_or_404(User, pk=pk)
    form = CreateProfileForm()
    if request.method =='POST':
        form = CreateProfileForm(instance=user.profile,data=request.POST,files=request.FILES, user=user)
        if form.is_valid():
            # post = form.save(commit=False)
            form.save()
            # comment = Comment.objects.create(post=form, author=request.user, body='')
        return redirect('profiledetail', pk=user.pk)
    else:
        form = CreateProfileForm(instance=user.profile)
    return render(request, "authentication/profiledetail.html", {"user":user,"form":form})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Đọc dữ liệu từ file excel
            dataset = Dataset()
            imported_data = dataset.load(request.FILES['file'].read(), format='xlsx')
            # Validate dữ liệu
            resource = UserResource()
            result = resource.import_data(imported_data, dry_run=True)
            if not result.has_errors():
                # Lưu dữ liệu vào database
                resource.import_data(imported_data)
                return HttpResponseRedirect(reverse('staff'))
            else:
                # Trả về thông báo lỗi
                return render(request, 'authentication/member.html', {'form_user': form, 'error': result.errors})
    else:
        form = UploadFileForm()
    return render(request, 'authentication/member.html', {'form_user': form})

def simple_upload(request):
    if request.method == 'POST':
        department_resource = UserResource()
        dataset = Dataset()
        new_department = request.FILES['my_file']
        if not new_department.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request,'upload.html')
        imported_data = dataset.load(new_department.read(),format='xlsx')
        for data in imported_data:
            
            # Kiểm tra user đã tồn tại chưa
            if User.objects.filter(username=data[3]).exists():
                continue
            # Thêm mới user
            new_user = User(
                # data[1],
                password=data[2],
                username=data[3],
                first_name=data[4],
                last_name=data[5],
                email=data[6],
                # data[7],
                # data[8], 
            )
            # user.password='hiep@123'
            new_user.last_login=None
            new_user.is_superuser=0
            new_user.is_staff=0
            new_user.is_active=1
            # new_profile = Profile(
            #     user=data[1],
            #     msnv=data[7],
            #     hovaten=data[8],
            #     phongban=data[9],
            #     chucdanh=data[10],
            #     gioitinh=data[11],
            #     ngaysinh=data[12],
            #     photo=data[17],
            #     phone=data[18],
            #     ngayvaocty=data[19],
            # )
            # new_profile.sophepnam=12
            # new_profile.songaynghiphep=0
            # new_profile.songaynghikhongphep=0
            # new_profile.songaynghiphepconlai=12
            
            new_user.save()
            # new_profile.save()

        messages.success(request, 'Đã thêm {} tài khoản thành công'.format(len(imported_data)))
    return render(request,'upload.html')

# def simple_upload(request):
#     if request.method == 'POST':
#         department_resource = UserResource()
#         dataset = Dataset()
#         new_department = request.FILES['my_file']
#         if not new_department.name.endswith('xlsx'):
#             messages.info(request,'wrong format')
#             return render(request,'upload.html')
#         imported_data = dataset.load(new_department.read(),format='xlsx')
#         for data in imported_data:
#             value = User(
#                 data[0],
#                 data[1],
#                 data[2],
#                 data[3],
#                 data[4],
#                 data[5],
#                 data[6],
#             )
#             value.save()
#     return render(request,'upload.html')