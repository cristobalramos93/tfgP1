from django.contrib import admin
from gestionPacientes.models import Usuarios, TipoIns, Medico, Paciente, Centro_medico, Tratamiento, Investigador, \
    Centro_investigacion
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

admin.site.register(Usuarios)
admin.site.register(TipoIns)
admin.site.register(Paciente)
admin.site.register(Centro_medico)
admin.site.register(Centro_investigacion)
admin.site.register(Tratamiento)

class UserCreationForm(forms.ModelForm):
    #A form for creating new users. Includes all the required
    #fields, plus a repeated password.
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        proxy = True
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    #A form for updating users. Includes all the fields on
    #the user, but replaces the password field with admin's
    #password hash display field.
    password = ReadOnlyPasswordHashField()

    class Meta:
        proxy = True
        fields = ('email', 'password')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class MedicoAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_active', 'is_staff')
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('username','first_name', 'last_name','email','password', 'board_number', 'medical_center')}),
        
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','first_name', 'last_name','email','password1', 'password2', 'board_number', 'medical_center')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
# Register your models here.

admin.site.register(Medico, MedicoAdmin)


class InvestigadorAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_active', 'is_staff')
    list_filter = ('email',)
    fieldsets = (
        (None,
         {'fields': ('username', 'first_name', 'last_name', 'email', 'password', 'Investigator_type', 'investigation_center')}),

    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'Investigator_type', 'investigation_center')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(Investigador, InvestigadorAdmin)