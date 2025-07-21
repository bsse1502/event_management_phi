from django import forms
from events.models import Event, Category, Participant
class StyledFormMixin:
    """Mixin to apply beautiful Tailwind styling to form fields."""

    base_input = (
        "w-full px-4 py-2 mt-1 border border-gray-300 rounded-xl shadow-sm "
        "focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 "
        "transition duration-150 ease-in-out text-sm bg-white"
    )

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            placeholder_text = f"Enter {field.label.lower()}"
            
            if isinstance(field.widget, forms.TextInput) or isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    "class": self.base_input,
                    "placeholder": placeholder_text
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    "class": f"{self.base_input} resize-none",
                    "placeholder": placeholder_text,
                    "rows": 5
                })
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({
                    "class": self.base_input,
                    "type": "date"
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    "class": self.base_input
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    "class": "flex flex-col gap-2 mt-2"
                })
            else:
                field.widget.attrs.update({
                    "class": self.base_input
                })


class CategoryModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        } 
        labels = {
            'name': 'Category Name',
            'description': 'Category Description',
        }  
    
    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

class ParticipantModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
        }
        labels = {
            'name': 'Participant Name',
            'email': 'Email Address',
        }
    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

class EventModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'location', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': 'Event Name',
            'date': 'Event Date',
            'location': 'Event Location',
            'description': 'Event Description',
        }
    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()