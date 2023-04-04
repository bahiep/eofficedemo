from django import forms
from .models import Comment, Post
# from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput


class CommentForm(forms.ModelForm):
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
        model = Comment
        fields = ['body']
        widgets={          
            'body':forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'3'}),
        }

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        title = forms.CharField(label="Tiêu đề")
        reason = forms.CharField()
        # date_from = forms.CharField(label="Nghỉ từ ngày:")
        date_end = forms.CharField(label="Đến ngày:")
        numday = forms.CharField(label="Số ngày nghỉ:")
        self.author = kwargs.pop('author', None)
        self.approval = kwargs.pop('approval', None)
        self.approvalbod = kwargs.pop('approvalbod', None)
        # self.post = kwargs.pop('post',None)
        super().__init__(*args, **kwargs)
    def save(self, commit=True):
        post=super().save(commit=False)
        post.author=self.author
        post.approval=self.approval
        post.approvalbod=self.approvalbod
        # comment.post = self.post
        post.save()
    class Meta:
        model = Post
        fields = ["date_from","date_end","numday","reason","title",] 
        widgets={          
            'reason':forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'2'}),
            'date_from': forms.DateInput(attrs={'class':'form-control form-control-sm','type': 'date'}),
            'date_end': forms.DateInput(attrs={'class':'form-control form-control-sm','type': 'date'}),
            'numday': forms.NumberInput(attrs={'class':'form-control form-control-sm'}),
            'title': forms.Select(attrs={'class':'form-control form-control-sm'})
        }