from django.urls import path,include
from Backend.views import index,product_list_view,category_list_view,\
    category_product_list_view,product_detail_view,tag_list,ajax_add_review,\
    search_view,filter_product,add_to_cart,cart_view,delete_item_from_cart,\
    update_cart,checkout_view,payment_completed_view,payment_failed_view,about,contact,contact_save


app_name = "Backend"


urlpatterns=[

    # Homepage
    path("",index, name="index"),

    # Products
    path("products/",product_list_view,name="product_list"),
    path("product/<pid>/",product_detail_view,name="product_detail"),

    # Category
    path("category/",category_list_view,name="category_list"),
    path("category/<cid>/",category_product_list_view,name="category_product_list"),

    # Tags
    path("products/tag/<slug:tag_slug>/",tag_list,name="tags"),

    #Add Review
    path("ajax_add_review/<int:pid>/",ajax_add_review,name="ajax_add_review"),

    #Search
    path("search/",search_view,name="search"),

    #Filter Products
    path("filter-products/",filter_product,name="filter-product"),

    #Add to cart
    path("add-to-cart/", add_to_cart, name="add-to-cart"),

    #Cart Page
    path("cart/", cart_view, name="cart"),

    #Delete item from cart
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),

    #Update Cart
    path("update-cart/", update_cart, name="update-cart"),

    #Checkout
    path("checkout/", checkout_view, name="checkout"),


    #Payment Successful
    path("payment-completed/", payment_completed_view, name="payment-completed"),

    #Payment Failed
    path("payment-failed/", payment_failed_view, name="payment-failed"),


    #Wishlist Page
    # path("wishlist/", wishlist_view, name="wishlist"),

    #Adding to wishlist
    # path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),

    # path("invoice_view/", invoice_view, name="invoice_view"),


    #About
    path("about/", about, name="about"),

    #Contact
    path("contact/", contact, name="contact"),
    path('contact_save/', contact_save, name='contact_save'),





]