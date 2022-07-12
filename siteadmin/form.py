from django import forms
from product.models import category, product, Variation, subcategory


class addproductform(forms.ModelForm):
        
    class Meta:
        
        model = product
        
        fields = ['product_name','slug','description','price','thumbnail_image_1','thumbnail_image_2','thumbnail_image_3','thumbnail_image_4','stock','category','subcategory',]
        
        widgets = {
            'product_name'            :forms.TextInput(attrs={ 'class': 'form-control',}),
            'slug'                    :forms.TextInput(attrs={ 'class': 'form-control',}),
            'description'             :forms.Textarea(attrs={ 'class': 'form-control',}),
            'price'                   :forms.NumberInput(attrs={ 'class': 'form-control',}),
            'stock'                   :forms.NumberInput(attrs={ 'class': 'form-control',}),
            'category'                :forms.Select(attrs={'class':'form-control'}),
            'subcategory'             :forms.Select(attrs={'class':'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = subcategory.objects.none()
        if 'category' in self.data:
            try:
                category = int(self.data.get('category'))
                self.fields['subcategory'].queryset = subcategory.objects.filter(category_id=category).order_by('id')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('id')
            
    
class addvariationform(forms.ModelForm):
    
    class Meta:
        
        model = Variation
        
        fields =['product','variation_category','variation_value',]
        
        widgets = {
            'product'                 :forms.Select(attrs={'class':'form-control'}),
            'variation_category'      :forms.Select(attrs={'class':'form-control'}),
            'variation_value'         :forms.TextInput(attrs={ 'class': 'form-control',}),
        }
        
class addcategoryform(forms.ModelForm):
    
    class Meta:
        
        model = category
        
        fields =['category_name','slug','description','cat_image']
        
        widgets = {
            'category_name'           :forms.TextInput(attrs={ 'class': 'form-control'}),
            'slug'                    :forms.TextInput(attrs={ 'class': 'form-control'}),
            'description'             :forms.TextInput(attrs={ 'class': 'form-control'}),
        }
        
class addsubcategoryform(forms.ModelForm):
    
    class Meta:
        model = subcategory
        fields =['subcategory','slug','category',]
        widgets = {
            'subcategory'          :forms.TextInput(attrs={ 'class': 'form-control'}),
            'slug'                 :forms.TextInput(attrs={ 'class': 'form-control'}),
            'category'             :forms.Select(attrs={ 'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = category.objects.all()