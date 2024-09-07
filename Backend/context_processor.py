from Backend.models import Product,Category,Vendor,CartOrder,CartOrderItems,ProductImages,wishlist_model,ProductReview,Address
from django.db.models import Min,Max
from django.contrib import messages


def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    min_max_price = Product.objects.aggregate(Min("price"),Max("price"))

    # try:
    #     wishlist = wishlist_model.objects.filter(user=request.user)
    # except:
    #     messages.warning(request,"You need to login before accessing your wishlist")
    #     wishlist = 0

    # address = Address.objects.get(user=request.user)


    return {
        "categories":categories,
        "vendors":vendors,
        "min_max_price":min_max_price,
        # "address":address,
    }