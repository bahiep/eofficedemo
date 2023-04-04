from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=50,label='Tên',widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50,label='Họ',widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = 'Tên tài khoản'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].label = 'Mật khẩu'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].label = 'Nhập lại mật khẩu'

class UserEditForm(forms.ModelForm):
    last_name = forms.CharField(label="Họ")
    first_name = forms.CharField(label="Tên")
    email = forms.EmailField(label="E-mail")
    class Meta:
        model = User
        fields = ( 'last_name','first_name', 'email')
class ProfileEditForm(forms.ModelForm):
    msnv = forms.CharField(label="MSNV")
    hovaten = forms.CharField(label="Họ và tên")
    phongban = forms.CharField(label="Phòng ban")
    chucdanh = forms.CharField(label="Chức danh")
    gioitinh = forms.CharField(label="Giới tính")
    ngaysinh = forms.DateField(label="Ngày sinh")
    photo = forms.ImageField(label="Ảnh đại diện")
    phone = forms.CharField(label="Số điện thoại")
    ngayvaocty = forms.DateField(label="Ngày vào công ty")
    class Meta:
        model = Profile
        # fields = ('msnv','hovaten', 'phongban','chucdanh','gioitinh','ngaysinh','photo','phone','ngayvaocty')
        fields = ('msnv','hovaten', 'gioitinh','ngaysinh','photo','phone','ngayvaocty')
        widgets={          
            'ngaysinh': forms.DateInput(attrs={'class':'form-control form-control-sm','type': 'date'}),
            'gioitinh': forms.Select(attrs={'class':'form-control form-control-sm'})
        }
class CreateProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        msnv = forms.CharField(label="MSNV")
        hovaten = forms.CharField(label="Họ và tên")
        phongban = forms.CharField(label="Phòng ban")
        chucdanh = forms.CharField(label="Chức danh")
        gioitinh = forms.CharField(label="Giới tính")
        ngaysinh = forms.DateField(label="Ngày sinh")
        photo = forms.ImageField(label="Ảnh đại diện")
        phone = forms.CharField(label="Số điện thoại")
        ngayvaocty = forms.DateField(label="Ngày vào công ty")
        self.user = kwargs.pop('user', None)
        # self.post = kwargs.pop('post',None)
        super().__init__(*args, **kwargs)
    def save(self, commit=True):
        post=super().save(commit=False)
        post.user=self.user
        # comment.post = self.post
        post.save()
    class Meta:
        model = Profile
        fields = ['msnv','hovaten', 'phongban','chucdanh','gioitinh','ngaysinh','photo','phone','ngayvaocty'] 
        widgets={  
            'hovaten': forms.TextInput(attrs={'class':'form-control form-control-sm'}), 
            'msnv': forms.TextInput(attrs={'class':'form-control form-control-sm'}), 
            'phongban': forms.Select(attrs={'class':'form-control form-control-sm'}),  
            'chucdanh': forms.Select(attrs={'class':'form-control form-control-sm'}),    
            'ngaysinh': forms.DateInput(attrs={'class':'form-control form-control-sm','type': 'date'}),
            'phone': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'gioitinh': forms.Select(attrs={'class':'form-control form-control-sm'}),
            
            'ngayvaocty': forms.DateInput(attrs={'class':'form-control form-control-sm','type': 'date'}),
        }

class UploadFileForm(forms.Form):
    file = forms.FileField()