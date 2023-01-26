from django import forms
from .models import LichHop, GhichuLichHop

class FormLichHop(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        title = forms.CharField(label="Tiêu đề")
        date = forms.DateField()
        time_from = forms.CharField(label="Từ:")
        time_end = forms.CharField(label="Đến:")
        num_per = forms.CharField(label="Số ngày nghỉ:")
        self.author = kwargs.pop('author', None)
        
        self.approval = kwargs.pop('approval', None)
        super().__init__(*args, **kwargs)
    def save(self, commit=True):
        post=super().save(commit=False)
        post.author=self.author
        
        post.approval=self.approval
        post.save()
    class Meta:
        model = LichHop
        fields = ["title","date","time_from","time_end","num_per","kind","room",] 
        widgets={          
            'title':forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'2'}),
            'date': forms.DateInput(attrs={'class':'form-control form-control-sm','type': 'date'}),
            'time_from': forms.TimeInput(attrs={'class':'form-control form-control-sm','type': 'time'}),
            'time_end': forms.TimeInput(attrs={'class':'form-control form-control-sm','type': 'time'}),
            'num_per': forms.NumberInput(attrs={'class':'form-control form-control-sm'}),
            'room': forms.Select(attrs={'class':'form-control form-control-sm'}),
            'kind': forms.Select(attrs={'class':'form-control form-control-sm'}),
            'link': forms.URLInput(attrs={'class':'form-control form-control-sm'}),
        }

class FormGhiChuLichHop(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        self.post = kwargs.pop('post',None)
        self.body = kwargs.pop('body','')
        self.status = kwargs.pop('status','')
        super().__init__(*args, **kwargs)
    def save(self, commit=True):
        comment=super().save(commit=False)
        comment.author = self.author
        comment.post = self.post
        comment.body = self.body
        comment.status = self.status
        comment.save()
    class Meta:
        model = GhichuLichHop
        fields = ['body']
        widgets={          
            'body':forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'3'}),
        }