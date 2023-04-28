from django import forms
import datetime
from apps.authentication.models import User 
class AskForm(forms.Form):
    
    userid = forms.IntegerField()
    username = forms.CharField(max_length=1000)
    time = forms.DateTimeField(initial=datetime.datetime.now())
    sentence = forms.CharField(widget=forms.TextInput(attrs={'class': 'special'}))
    tags= forms.CharField(widget=forms.TextInput(attrs={'class': 'special'}))
class Anno(forms.Form):
    CHOICES = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
        ('4', 'Option 4'),
        ('5', 'Option 5'),
        ('6', 'Option 6'),
        ('7', 'Option 7'),
        ('8', 'Option 8'),
        ('9', 'Option 9'),
        ('10', 'Option 10'),  
        ('11','Option 11'),
    ]
    option = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES, 
    )
    textinp = forms.CharField( max_length=50, required=False)
# class UploadExcel(forms.Form):

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label='Select an Excel file')
    datasetname = forms.CharField(max_length=1000)
class TaskChangeForm(forms.Form):
    users = User.objects.all()
    user_id = forms.ModelChoiceField(queryset=users)
    tasks = [('Task 1', 'Task 1'), ('Task 2', 'Task 2'), ('Task 3', 'Task 3')]
    lowerbound = forms.IntegerField