# views.py

from django.shortcuts import render, redirect
from .forms import SlaughterForm

def slaughter_breeds(request):
    if request.method == 'POST':
        form = SlaughterForm(request.POST)
        if form.is_valid():
            breeds_selected = form.cleaned_data['breeds_to_slaughter']
            # Update store - deduct quantities of selected breeds
            for breed in breeds_selected:
                breed.breeds_supplied -= 1  # Adjust quantity as needed
                breed.save()
            return redirect('store_updated_successfully')  # Redirect to success page
    else:
        form = SlaughterForm()
    return render(request, 'slaughter_form.html', {'form': form})
