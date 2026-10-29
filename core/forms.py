
from django import forms


class BaseModelForm(forms.ModelForm):

    base_classes = (
        "bg-base text-content border border-stroke-soft px-4 py-2 mt-1 rounded-lg "
        "focus:ring-2 transition duration-200 outline-none w-full shadow-sm"
    )


    error_classes = "border-red-500 focus:ring-red-500 text-red-600"

    class Meta:
        model = None
        fields = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_design_system()

    def apply_design_system(self):
        for field_name, field in self.fields.items():

            existing = field.widget.attrs.get('class', '')
            current_classes = self.base_classes
            if self.errors.get(field_name):
                current_classes += f" {self.error_classes}"

            field.widget.attrs['class'] = f"{existing} {current_classes}".strip()
