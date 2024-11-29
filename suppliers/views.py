from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from .models import Supplier
from .forms import SupplierForm
from django.contrib import messages
from django.db.models import Q

def index(request):
    search_query = request.GET.get('search', '')
    if search_query:
        suppliers = Supplier.objects.filter(
            Q(id__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(supplier_hardware__icontains=search_query)
        ).order_by('id')
        results_count = suppliers.count()
        messages.info(request, f"{results_count} results found.")
    else:
        suppliers = Supplier.objects.all().order_by('id')
        results_count = 0

    return render(request, 'suppliers/index.html', {
        'suppliers': suppliers,
        'results_count': results_count 
    })


def view_supplier(request, id):
    supplier = Supplier.objects.get(pk=id)
    return HttpResponseRedirect(reverse('index'))

def add(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            # Create a new supplier from the form data
            new_supplier = form.save()
            return render(request, 'suppliers/add.html', {
                'form': SupplierForm(),  # Reset the form after successful submission
                'success': True  # Indicate success
            })
        else:
            # If the form is not valid, return it with errors
            return render(request, 'suppliers/add.html', {
                'form': form  # Pass the form with errors back to the template
            }) 
    else:
        # For GET requests, display a blank form
        form = SupplierForm()
        return render(request, 'suppliers/add.html', {
            'form': form
        })

def delete(request, id):

    supplier = get_object_or_404(Supplier, id=id)
    
    if request.method == 'POST':
        supplier = Supplier.objects.get(pk=id)
        messages.success(request, 'Supplier deleted successfully.')
        supplier.delete()
    return HttpResponseRedirect(reverse('suppliers_index'))

def edit(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('suppliers_index')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/edit.html', {'form': form, 'supplier': supplier})