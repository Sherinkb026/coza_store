
# Create your views here.
from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from taggit.models import Tag
from django.db.models import Avg
from Backend.models import Product,Category,Vendor,CartOrder,CartOrderItems,ProductImages,wishlist_model,ProductReview,Address,ContactUs
from Backend.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.contrib import messages
import razorpay
from django.conf import settings
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required




# Create your views here.

def index(request):
    # products = Product.objects.all().order_by("-id")                                    #Filter query
    products = Product.objects.filter( featured=True)
    context = {
        "products":products
    }
    return render(request, 'backend/index.html',context)


def product_list_view(request):
    products = Product.objects.filter(featured=True)
    context = {
        "products": products
    }
    return render(request, 'backend/product_list.html', context)


def category_list_view(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, 'backend/category_list.html', context)


def category_product_list_view(request,cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(featured=True,category=category)

    context = {
        "category":category,
        "products":products,


    }
    return render(request,"Backend/category_product_list.html", context)


def product_detail_view(request,pid):
    product = Product.objects.get(pid=pid)

    p_image = product.p_image.all()
    size = [choice[1] for choice in product._meta.get_field('size').choices]
    color = [choice[1] for choice in product._meta.get_field('color').choices]
    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    # Getting all reviews
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
   # Getting average reviews
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    #Product Review Form

    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user,product=product).count()
        if user_review_count>0:
            make_review = False


    context = {
        "p":product,
        "p_image":p_image,
        "size":size,
        "color":color,
        "products":products,
        "reviews":reviews,
        "average_rating":average_rating,
        "review_form":review_form,
        "make_review":make_review,

    }

    return render(request,"Backend/product_detail.html", context)


def tag_list(request, tag_slug=None):
    products = Product.objects.filter(featured=True).order_by("-id")
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

        context = {
            'products':products,
        }

        return render(request,"Backend/tag.html", context)


def ajax_add_review(request,pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],


    )

    context = {
        'user':user.username,
        'review' : request.POST['review'],
        'rating' : request.POST['rating'],
        }


    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
    return JsonResponse(
        {
            'bool': True,
         'context': context,
         'average_reviews': average_reviews,
        }

    )


def search_view(request):
    query = request.GET.get("q")
    products = Product.objects.filter(title__icontains=query).order_by("-date")

    context = {
        'products':products,
        'query':query,
    }

    return render(request, 'backend/search.html', context)


def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(featured=True).order_by("-id").distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)


    if len(categories)>0:
        products = products.filter(category__id__in=categories).distinct()


    if len(vendors)>0:
        products = products.filter(vendor__id__in=vendors).distinct()

    data = render_to_string("backend/async/product_list.html", {"products":products})

    return JsonResponse({"data":data})


def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title':request.GET['title'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
        'image':request.GET['image'],
        'pid':request.GET['pid'],

    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj']  = cart_product

    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})


def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            try:
                qty = int(item.get('qty', 0))
                price = float(item.get('price', 0))
                cart_total_amount += qty * price
            except ValueError:
                # Handle the case where qty or price are not valid numbers
                messages.error(request, f"Invalid data for product ID {p_id}.")
                continue

        return render(request, "Backend/cart.html", {
            "cart_data": request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount
        })
    else:
        messages.warning(request, "Your Cart is Empty")
        return redirect("Backend:index")


def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("backend/async/cart_list.html",{"cart_data": request.session['cart_data_obj'],
                                                   'totalcartitems': len(request.session['cart_data_obj']),
                                                   'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})


def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("backend/async/cart_list.html",{"cart_data": request.session['cart_data_obj'],
                                                   'totalcartitems': len(request.session['cart_data_obj']),
                                                   'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})




@login_required
def checkout_view(request):
    cart_total_amount = 0
    total_amount = 0
    if 'cart_data_obj' in request.session:

        #Getting total amount for the cart
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])

        #Create order objects
        order = CartOrder.objects.create(
            user = request.user,
            price = total_amount
        )
        #Getting total amount for the cart
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            cart_order_products = CartOrderItems.objects.create(
                order = order,
                invoice_no = "INVOICE_NO-" + str(order.id),
                item = item['title'],
                image = item['image'],
                qty = item['qty'],
                price = item['price'],
                total = float(item['qty']) * float(item['price'])
            )





    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    if request.method == "POST":
        client = razorpay.Client(auth=(settings.rzp_test_yg9PswGjLhzEZi, settings.m9pPbPl4sqGQCnvWLPqShfsi))
        payment_data = {
            'amount': int(cart_total_amount * 100),  # Amount should be in paise
            'currency': 'INR',
            'receipt': 'order_receipt_' + str(request.user.id),  # Unique receipt ID
            'payment_capture': 1  # Auto-capture payment
        }
        payment = client.order.create(data=payment_data)

        # Optionally, save the order ID or other payment details to your database

        return JsonResponse({'order_id': payment['id']})

    context = {
        'cart_data': request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_total_amount': cart_total_amount,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID
    }
    return render(request, "Backend/checkout.html", context)


@login_required()
def payment_completed_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    # Gather data for rendering the template
    context = {
        'cart_data': request.session.get('cart_data_obj', {}),
        'totalcartitems': len(request.session.get('cart_data_obj', {})),
        'cart_total_amount': cart_total_amount,
        'razorpay_key_id': settings.rzp_test_yg9PswGjLhzEZi,
        'request': request,
    }

    # Render the invoice template to HTML
    invoice_html = render_to_string("Backend/payment_completed.html", context)

    # Create PDF
    pdf = HttpResponse(content_type='application/pdf')
    pdf['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    pisa.CreatePDF(invoice_html, dest=pdf)

    # Return the PDF as a response
    return pdf


@login_required()
def payment_failed_view(request):
    return render(request,'backend/payment_failed.html')

# @login_required()
# def wishlist_view(request):
#     wishlist = wishlist_model.objects.all()
#     context = {
#         "w":wishlist,
#     }
#
#     return render(request,"Backend/wishlist.html", context)



# @login_required()
# def add_to_wishlist(request):
#     product_id=request.GET['id']
#     product = Product.objects.get(id=product_id)
#     print("product id is:", +product_id)
#
#     context = {}
#
#     wishlist_count = wishlist_model.objects.filter(product=product, user=request.user).count()
#     print(wishlist_count)
#
#
#     if wishlist_count > 0:
#         context = {
#             "bool":True
#         }
#     else:
#         new_wishlist = wishlist_model.objects.create(
#             product=product,
#             user=request.user
#         )
#
#         context = {
#             "bool":True
#         }
#
#     return JsonResponse(context)



def about(request):
    return render(request,"Backend/about.html")


def contact(request):
    return render(request,"Backend/contact.html")

def contact_save(request):
    if request.method=="POST":
        e=request.POST.get("email")
        m=request.POST.get("msg")
        obj=ContactUs(mail=e,message=m)
        obj.save()
        return redirect("Backend:contact")






























