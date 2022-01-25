from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.six import text_type
from .models import commentModel_1,userProfileModel,questionModel,itemModel

class addProductForm(ModelForm):
    class Meta():
        model = itemModel
        fields = ['item_id','item_name','item_discription','item_Price','item_offer','in_stoke','sold_by','quality','slug']
class productImageForm(ModelForm):
    class Meta():
        model =itemModel
        fields = ['item_image',]

 
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=256,help_text='Required')
    
    # phone_no = forms.CharField(max_length = 20)
    # first_name = forms.CharField(max_length = 20)
    # last_name = forms.CharField(max_length = 20)
    class Meta():
        model = User
        fields = ['username', 'email', 'password1', 'password2',]

    # profile_pic = forms.ImageField()

################################## comment form #####################################
class commentForm_1(ModelForm):
    # author = User.username
    # print(User.username)
    class Meta():
        model = commentModel_1
        fields =['comment',]

class questionForm(ModelForm):
    class Meta():
        model= questionModel
        fields =['question',]

class profileForm(ModelForm):
    class Meta():
        model = userProfileModel
        fields = ['userpic',]

        


