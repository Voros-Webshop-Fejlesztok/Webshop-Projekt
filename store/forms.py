from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post, Customer, Message


from .models import Order

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    title = forms.CharField(required=True,
        widget=forms.widgets.Textarea(
            attrs={"placeholder":"Poszt címe",
                   "class":"form-textarea",
                   'cols':'40',
                   'rows':'1',
                   'maxlength':'50',
                   'required':'required',}),
        label="")
    body = forms.CharField(required=True,
        widget=forms.widgets.Textarea(
            attrs={"placeholder":"Mi jár a fejedben?",
                   "class":"form-textarea",
                   'cols':'65',
                   'rows':'10',
                   'maxlength':'1000',
                   'required':'required',}),
        label="")
    
    class Meta:
        model = Post
        exclude = ("user",)

class UpdateProfileForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "style": "width:300px",
            "placeholder": "Teljes név",
            "class": "form-input",
            "maxlength": "30",
            'cols':'40',
            'rows':'1',
            "required": "required",
        }),
        label=""
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "style": "width:280px",
            "placeholder": "Email cím",
            "class": "form-input",
            "maxlength": "40",
            'cols':'40',
            'rows':'1',
            "required": "required",
        }),
        label=""
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "style": "width:280px",
            "placeholder": "Telefonszám",
            "class": "form-input",
            'cols':'40',
            'rows':'1',
            "maxlength": "20",
        }),
        label=""
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "placeholder": "Bio",
            "class": "form-textarea",
            "cols": "40",
            "rows": "4",
            "maxlength": "500",
        }),
        label=""
    )
    image = forms.ImageField(label='Profile Picture')

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_number', 'image', 'description', 'image']

class DeletePostForm(forms.Form):
    post_id = forms.IntegerField()
class DeleteMessageForm(forms.Form):
    message_id = forms.IntegerField()

class SendMessage(forms.ModelForm):
    content = forms.CharField(required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder":"Üzenet küldése",
                   "class":"form-textarea",
                   'cols':'40',
                   'rows':'1',
                   'maxlength':'1000',
                   'required':'required',
                   'id':'chatInput',
                   }),
        label="")
    
    class Meta:
        model = Message
        fields = ['content']
        exclude = ("user", 'sender', 'receiver',)