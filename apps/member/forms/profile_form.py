# -*- coding: utf-8 -*-
try:
    import json
except:
    from django.utils import simplejson as json

from django import forms
from apps.member.models import Member

class ProfileForm(forms.Form):
    realname = forms.CharField(label=u'真实姓名/Name', required=True, max_length=20, widget=forms.TextInput(attrs={'tabindex': '1'}))
    gender = forms.ChoiceField(label=u'性别/Gender', required=True, choices=((u'男', u'男'), (u'女', u'女'), (u'中性', u'中性')), widget=forms.Select(attrs={'tabindex': '2'}))
    career_years = forms.ChoiceField(label=u'工作年限/Career', required=True, choices=((u'1-3年', u'1-3年'), (u'3-5年', u'3-5年'), (u'5年以上', u'5年以上')), widget=forms.Select(attrs={'tabindex': '3'}))

    company = forms.CharField(label=u'公司/Company', required=False, max_length=40, widget=forms.TextInput(attrs={'tabindex': '4'}))
    position = forms.CharField(label=u'职位/Position', required=False, max_length=30, widget=forms.TextInput(attrs={'tabindex': '5'}))
    blog = forms.CharField(label=u'博客/Blog', required=False, max_length=255, widget=forms.TextInput(attrs={'tabindex': '6'}))
    phone = forms.CharField(label=u'手机/Phone', required=False, max_length=255, widget=forms.TextInput(attrs={'tabindex': '6'}))

    hobby = forms.CharField(label=u'兴趣/hobby', required=False, max_length=255, widget=forms.TextInput(attrs={'tabindex': '6'}))

    gtalk = forms.CharField(label=u'Gtalk', required=False, max_length=127, widget=forms.TextInput(attrs={'tabindex': '6'}))
    msn = forms.CharField(label=u'Msn', required=False, max_length=127, widget=forms.TextInput(attrs={'tabindex': '6'}))
    twitter = forms.CharField(label=u'twitter', required=False, max_length=127, widget=forms.TextInput(attrs={'tabindex': '6'}))
    foursquare = forms.CharField(label=u'foursquare', required=False, max_length=127, widget=forms.TextInput(attrs={'tabindex': '6'}))
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        self.member = Member.objects.get(user=self.user)
        if (not args) and (not kwargs) and self.member and self.member.properties:
            properties = {}
            for key, value in json.loads(self.member.properties).items():
                properties[key.encode('utf-8')] = value.encode('utf-8')
            super(ProfileForm, self).__init__(properties)
        else:
            super(ProfileForm, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data
    
    def save(self):
        if not self.is_valid():
            return False

        if not self.member:
            return False
        
        properties = json.dumps(self.cleaned_data)
        self.member.properties = properties

        self.member.save()
        return self.member
