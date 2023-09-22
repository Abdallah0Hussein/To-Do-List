from django import forms
from django.forms import ModelForm
from .models import Task
from django.utils import timezone
from django.forms.widgets import DateInput
from django.forms.widgets import DateTimeInput

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ' Add a New Task', 'style': 'width: 500px;'}))
    priority = forms.ChoiceField(
        choices=[
            ("Low", "Low"),
            ("Medium", "Medium"),
            ("High", "High"),
        ],
        widget=forms.Select()
    )
    deadline = forms.DateTimeField(
    widget=DateTimeInput(
        attrs={"type": "datetime-local"},
    ),
    initial=timezone.now
)

    # Define a custom validation method for the 'deadline' field
    def clean_deadline(self):
        # get the deadline from the user then check the normal validatation of it
            deadline = self.cleaned_data.get('deadline')
            if deadline <= timezone.now():
                raise forms.ValidationError("The deadline must be in the future.")
            return deadline
