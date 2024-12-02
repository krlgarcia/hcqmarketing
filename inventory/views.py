from django.shortcuts import render
from .models import Inventory  # Import Inventory model
from django.shortcuts import get_object_or_404
from inventory.models import StockHistory
from django.shortcuts import render, get_object_or_404
from .models import Inventory, StockHistory, SerializedInventory
from products.models import Product
from django.contrib import messages
from django.db.models import Q

def inventory_index(request):
    search_query = request.GET.get('search', '')
    if search_query:
        inventories = Inventory.objects.filter(
            Q(product__product_code__icontains=search_query) |
            Q(product__product_name__icontains=search_query) |
            Q(product__product_descript__icontains=search_query)
        ).order_by('id')
        results_count = inventories.count()
        messages.info(request, f"{results_count} result(s) found for '{search_query}'.")
    else:
        inventories = Inventory.objects.all().order_by('id')
        results_count = 0

    return render(request, 'inventory/index.html', {
        'inventories': inventories,
        'results_count': results_count 
    })


def product_detail(request, product_id):
    inventory = get_object_or_404(Inventory, product__id=product_id)
    stock_history = StockHistory.objects.filter(inventory=inventory).order_by('-timestamp')
    
    # Include serialized items if the product has serialized stock
    serialized_items = None
    if hasattr(inventory.product, 'is_serialized') and inventory.product.is_serialized:
        serialized_items = SerializedInventory.objects.filter(inventory=inventory)
        print(f"Serialized items found: {serialized_items}")  # Debugging line

    return render(request, 'inventory/product_detail.html', {
        'inventory': inventory,
        'stock_history': stock_history,
        'serialized_items': serialized_items,
    })