console.log("working fine");

const monthNames = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];

$("#commentForm").submit(function(e){
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDay()+ " " + monthNames[dt.getUTCMonth()]+ ", " +dt.getFullYear()

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType:"json",
        success:function(res){
            console.log("Comment save to DB...");

            if(res.bool==true){
                $("#review-res").html("Review Added Succesfully")
                $(".hide-comment-form").hide()

                let _html= '<div class="flex-w flex-t p-b-68" style="margin-top:20px;">';
					_html += '<div class="wrap-pic-s size-109 bor0 of-hidden m-r-18 m-t-6">';
                    _html += '<img src="data:image/png;base64,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" alt="AVATAR">';
                    _html += '</div>';

				    _html += '<div class="size-207">';
					_html += '<div class="flex-w flex-sb-m p-b-17">';
					_html += '<span class="mtext-107 cl2 p-r-20">'+ res.context.user +'</span><br>';
					_html += '<span class="mtext-107 cl2 p-r-20" style="color:#404040">'+ time +'</span>';
					for(let i=1;i<=res.context.rating;i++){
					    _html+= '<i class="fas fa-star text-warning"></i>';
					}

					_html += '</div>';

					_html += '<p class="stext-102 cl6">'+ res.context.review +'</p>';
					_html += '</div>';

					_html += '</div>';

					 $(".comment-list").prepend(_html)

                }


        }

    })
})


$(document).ready(function(){
    $(".filter-checkbox, .price-filter-btn").on("click", function(){
        console.log("A Checkbox have been clicked");

        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

//            console.log("Filter value is:" + filter_value);
//            console.log("Filter key is:" + filter_key);


            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
                return element.value
            })
        })

        console.log("Filter object is: ", filter_object)

        $.ajax({
            url:'/filter-products',
            data:filter_object,
            dataType:'json',
            beforeSend:function(){
                console.log("Trying to filter product...");
            },
            success:function(response){
                console.log(response);
                console.log("Data Filtered Successfully...");
                $("#filtered-product").html(response.data)
            }

        })
    })

    $("#max_price").on("blur", function(){
          let min_price = $(this).attr("min");
          let max_price = $(this).attr("max");
          let current_price = $(this).val();

//          console.log("Current Price is :",current_price);
//          console.log("Max Price is :",max_price);
//          console.log("Min Price is :",min_price);

          if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){


            min_price = Math.round(min_price * 100) / 100;
            max_price = Math.round(max_price * 100) / 100;





              alert("price must be between ₹" + min_price + ' and ₹ ' + max_price);
              $(this).val(min_price);
              $('#range').val(min_price);

              $(this).focus();

              return false;


          }
    })

    //Add to cart functionality
    $(".add-to-cart-btn").on("click",function(){

    let this_val = $(this)
    let index = this_val.attr("data-index")

    let quantity = $(".product-quantity-" + index).val()
    let product_title = $(".product-title-" +index).val()
    let product_id = $(".product-id-" + index).val()
    let product_price = $(".current-product-price-" + index).text().trim();
    let product_pid = $(".product-pid-" + index).val()
    let product_image = $(".product-image-" + index).val()



    console.log("Quantity:", quantity);
    console.log("Title:", product_title);
    console.log("Price:", product_price);
    console.log("ID:", product_id);
    console.log("PID:", product_pid);
    console.log("Image:", product_image);
    console.log("Index:", index);
    console.log("Current Element:", this_val);


    $.ajax({
        url:'/add-to-cart',
        data:{
            'id':product_id,
            'pid':product_pid,
            'image':product_image,
            'qty':quantity,
            'title':product_title,
            'price':product_price,
        },

        dataType:'json',
        beforeSend: function(){
            console.log("Adding Product to Cart...")
        },
        success:function(response){
        this_val.html("Item added to cart")
        console.log("Succesfully Added Product to Cart!")
        $(".cart-items-count").text(response.totalcartitems)
        }
    })



})

    $(document).on("click", '.delete-product', function(event){
        event.preventDefault();
        let product_id = $(this).attr("data-product")
        let this_val = $(this)

        console.log("Product ID:", product_id);

        $.ajax({
            url:"/delete-from-cart",
            data:{
                "id":product_id
            },
            dataType:'json',
            beforeSend:function(){
                this_val.hide()
            },

            success:function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)

            }


        })


    })


    $(document).on("click", '.update-product', function(event){
        event.preventDefault();
        let product_id = $(this).attr("data-product");
        let this_val = $(this);
        let product_quantity = $(".product-qty-" + product_id).val();

        console.log("Product ID:", product_id);
        console.log("Product QTY:", product_quantity);

        $.ajax({
            url: "/update-cart",
            data: {
            "id": product_id,
            "qty": product_quantity
        },
            dataType: 'json',
            beforeSend: function() {
                this_val.hide();
            },
            success: function(response) {
            this_val.show();
            $(".cart-items-count").text(response.totalcartitems);
            $("#cart-list").html(response.data);
        }
        });
    });



        //Adding to wishlist

    $(document).on("click", ".add-to-wishlist", function(){
        let product_id = $(this).attr("data-product-item");
        let this_val = $(this);

        console.log("Product ID is:", product_id);

        $.ajax({
            url: "/add-to-wishlist",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function() {
            console.log("Adding to wishlist...")


            },
            success: function(response) {
                this_val.html("✅");
                if (response.bool === true){
                    console.log("Added to Wishlist")

                }

            }
        });
    });






})







