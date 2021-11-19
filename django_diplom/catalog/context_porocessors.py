from catalog.models import Category


def nav_items_processor(request):
    categories = Category.objects.all()
    return {
        'nav_items': categories
    }
