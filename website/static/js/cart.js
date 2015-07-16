$(document).ready(function(){
	function updateCart(productId, qty) {
	$.ajax({
		type: "POST",
		url: "/shopping-cart/update_cart/",
		data: {"id": productId, "qty": qty, "csrfmiddlewaretoken": getCookie('csrftoken')},
		success: function(data){
			//message Success to user
			$('#theCart').html(data['quantity'] + ' ' + data['append'] + ' | ' + data['total']+ ' ' + data['currency']);
			$('#cart-dropdown').html(data['html']);
			if(data['valid'] == true){
			$.iGrowl({
			 type: 'success',
			 message: 'Your cart has been updated!',
			 icon: 'vicons-cart',
			 small: 'true',
			 placement : {
			  x: 	'right'
			 },
			  offset : {
			  y: 	100
			 },
			 animShow: 'fadeInLeftBig',
			 animHide: 'fadeOutDown',

			})
				
			}
			else{
				$.iGrowl({
				 type: 'notice',
				 message: 'The requested quantity exceeds the available stock',
				 icon: 'vicons-cart',
				 small: 'true',
				 placement : {
				  x: 	'right'
				 },
				  offset : {
				  y: 	100
				 },
				 animShow: 'fadeInLeftBig',
				 animHide: 'fadeOutDown',
				 })
			
		}
			
		}

	})
	}

	function deleteAllThisFromCart(productId) {
	$.ajax({
		type: "POST",
		url: "/shopping-cart/removeallthis/",
		data: {"id": productId, "csrfmiddlewaretoken": getCookie('csrftoken')},
		success: function(data){
			if(data['quantity'] > 0){
				$('#theCart').html(data['quantity'] + ' ' + data['append'] + ' | ' + data['total']+ ' ' + data['currency']);
			}
			else{
				$('#theCart').html('Empty Cart');
			}
			$('#cart-dropdown').html(data['html']);
			$.each(data['cart_quantities'], function( index, value ) {
			  $('#amount-input-'+index).val(value);
			});
			return true;

		}

	})
	}

	function emptyCart(){
		$.ajax({
			type: "POST",
			url: "/shopping-cart/empty_cart/",
			data: {"csrfmiddlewaretoken": getCookie('csrftoken')},
			success: function(){
				$('#theCart').html('Empty Cart');
				$('#cart-dropdown').html(data['html']);
				$.each(data['cart_quantities'], function( index, value ) {
			  		$('#amount-input-'+index).val(value);
				});
				return true;
		}

	})
	}



	function getOrderDetails(productId) {
	$.ajax({
		type: "POST",
		url: "/order_products/",
		data: {"id": productId, "csrfmiddlewaretoken": getCookie('csrftoken')},
		success: function(data){
			$('#modal-body').html(data['html']);
			return true;

		}

	})
	}

	// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$("a.emptyCart").click(function(){
	return emptyCart();
})

$(document).on('click', '.deleteAllThisFromCart', function(event){
	return deleteAllThisFromCart(this.id);
})

$(document).on('click', '.viewOrderDetails', function(event){
	return getOrderDetails(this.id);
})

$(".input-small").keydown(function (e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
             // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) || 
             // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }

    })

$(".input-small").keyup(function (e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
             // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) || 
             // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
        else{
        	var inputId = this.id;
        	inputId = inputId.replace('amount-input-','');
        	updateCart(inputId, $(this).val());
    	}
    })



});