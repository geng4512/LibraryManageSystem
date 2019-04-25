from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label="姓名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))

class SearchForm(forms.Form):
    bookname = forms.CharField(label="图书名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))

class ISBNForm(forms.Form):
    ISBN = forms.CharField(label="ISBN码", max_length=13, widget=forms.TextInput(attrs={'class': 'form-control'}))

class ReviewForm(forms.Form):
    ISBN = forms.CharField(label="ISBN码", max_length=13, widget=forms.TextInput(attrs={'class': 'form-control'}))
    score = forms.IntegerField(label="评分(请输入1-5的整数)", min_value=1, max_value=5, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    comment = forms.CharField(label="评论", max_length=300, widget=forms.TextInput(attrs={'class': 'form-control'}))