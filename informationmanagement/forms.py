from django import forms
from .models import Information, Year, Semester

class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = '__all__'

    course_level_type = forms.ChoiceField(
        choices=[('Year', 'Year'), ('Semester', 'Semester')],
        widget=forms.Select(attrs={'id': 'course_level_type'})
    )
    years = forms.ModelMultipleChoiceField(
        queryset=Year.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'id': 'year_options'})
    )
    semesters = forms.ModelMultipleChoiceField(
        queryset=Semester.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'id': 'semester_options'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['years'].queryset = Year.objects.none()
        self.fields['semesters'].queryset = Semester.objects.none()

        if self.instance and self.instance.pk:
            if self.instance.course_level_type == 'Year':
                self.fields['years'].queryset = Year.objects.all()
            elif self.instance.course_level_type == 'Semester':
                self.fields['semesters'].queryset = Semester.objects.all()
