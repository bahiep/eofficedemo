from django import forms
from .models import LichHop, GhichuLichHop
from datetime import datetime, timedelta

class FormLichHop(forms.ModelForm):
    time_from = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    time_end = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))

    def __init__(self, *args, **kwargs):
        title = forms.CharField(label="Tiêu đề")
        date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}))
        time_from = forms.ChoiceField(choices=[], required=True, label="Từ:", widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
        time_end = forms.ChoiceField(choices=[], required=True,label="Đến:", widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
        num_per = forms.CharField(label="Số ngày nghỉ:")
        self.author = kwargs.pop('author', None)
        self.approval = kwargs.pop('approval', None)
        super().__init__(*args, **kwargs)
        # Khởi tạo list chứa các lựa chọn giờ bắt đầu cách nhau 30 phút
        start_times = []
        start_times.append(('--:--', '--:--'))
        start = datetime.strptime('07:00', '%H:%M')
        end = datetime.strptime('18:00', '%H:%M')
        while start <= end:
            start_times.append((start.time().strftime('%H:%M'), start.strftime('%H:%M')))
            start += timedelta(minutes=30)

        # Thiết lập giá trị cho trường time_from
        self.fields['time_from'].choices = start_times
        self.fields['time_end'].choices = start_times

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

# from datetime import datetime, timedelta

# class MeetingRoomForm(forms.ModelForm):
#     start_time = forms.ChoiceField(choices=[], required=True)
#     end_time = forms.ChoiceField(choices=[], required=True)
#     class Meta:
#         model = MeetingRoom
#         fields = ['date', 'start_time', 'end_time', 'description', 'num_attendees']
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Khởi tạo list chứa các lựa chọn giờ bắt đầu cách nhau 30 phút
#         start_times = []
#         end_times = []
#         start = datetime.strptime('08:00', '%H:%M')
#         end = datetime.strptime('20:00', '%H:%M')
#         while start <= end:
#             start_times.append((start.time().strftime('%H:%M'), start.strftime('%H:%M')))
#             end_times.append((start.time().strftime('%H:%M'), start.strftime('%H:%M')))
#             start += timedelta(minutes=30)

#         # Thiết lập giá trị cho trường start_time
#         self.fields['start_time'].choices = start_times
#         self.fields['end_time'].choices = start_times