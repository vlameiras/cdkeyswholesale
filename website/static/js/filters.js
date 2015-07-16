    function resetAllValues() {
    $('#filter').val('');
    
    $('#platformFilter').prop('selectedIndex',0);
    $('#regionFilter').prop('selectedIndex',0);
    $('#languageFilter').prop('selectedIndex',0);
    $('#availabilityFilter').prop('selectedIndex',0);

    $('#filter').keyup();
}
	$(document).ready(function () {


function getOrderWithProducts(productId) {
    $.ajax({
        type: "GET",
        url: "/order_with_products/",
        data: {"product_name": productId},
        success: function(data){
            //$('#modal-body').html(data['html']);
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

    (function ($) {


$('#fileupload').bind('fileuploadsubmit', function (e, data) {

    var input_product = $('#productsList');
    var input_supplier = $('#suppliersList');
    var input_bundle = $('#bundle');
    var input_price = $('#price');
    //var input_margin = $('#margin');

    data.formData = {product_id: input_product.val(),
        supplier_id: input_supplier.val(),
        bundle: input_bundle.val(),
        price: input_price.val(),
        csrfmiddlewaretoken: getCookie('csrftoken')};
   
    if (!data.formData.product_id) {
      data.context.find('button').prop('disabled', false);
      input.focus();
      return false;
    }
    else if (!data.formData.supplier_id) {
      data.context.find('button').prop('disabled', false);
      input.focus();
      return false;
    }
    else if (!data.formData.bundle) {
      data.context.find('button').prop('disabled', false);
      input.focus();
      return false;
    }
    else if (!data.formData.price) {
      data.context.find('button').prop('disabled', false);
      input.focus();
      return false;
    }
    /*else if (!data.formData.margin) {
      data.context.find('button').prop('disabled', false);
      input.focus();
      return false;
    }*/
});

        $('#productsList').on('change', function (e) {
            //console.log($('input#productId').val());
          //  $('input#productId').val('9');
            //console.log($('input#productId').val());
        });


        $('#filterGameProduct').keyup(function () {
            var rex = new RegExp($(this).val(), 'i');
            $('.searchable tr').hide();
            $('.searchable tr').filter(function () {
                return rex.test($(this).text());
            }).show();

        })

        $('#filter').keyup(function () {

            var rex = new RegExp($(this).val(), 'i');
            var rex2 = new RegExp($('#platformFilter').val(), 'i');
            var rex3 = new RegExp($('#regionFilter').val(), 'i');
            var rex4 = new RegExp($('#languageFilter').val(), 'i');
            var rex5 = new RegExp($('#availabilityFilter').val());
            /*#console.log(rex2);*/
            $('.searchable tr').hide();
            $('.searchable tr').filter(function () {
                return rex.test($(this).text()) && rex2.test($(this).text()) && rex3.test($(this).text()) && rex4.test($(this).text()) && rex5.test($(this).text());
            }).show();

        })

        $('#platformFilter').change(function () {
            var rex = new RegExp($(this).val(), 'i');
            var rex2 = new RegExp($('#filter').val(), 'i');
            var rex3 = new RegExp($('#regionFilter').val(), 'i');
            var rex4 = new RegExp($('#languageFilter').val(), 'i');
            var rex5 = new RegExp($('#availabilityFilter').val());
            $('.searchable tr').hide();
            $('.searchable tr').filter(function () {
                return rex.test($(this).text()) && rex2.test($(this).text()) && rex3.test($(this).text()) && rex4.test($(this).text()) && rex5.test($(this).text());
            }).show();

        })

        $('#regionFilter').change(function () {
            var rex = new RegExp($(this).val(), 'i');
            var rex2 = new RegExp($('#filter').val(), 'i');
            var rex3 = new RegExp($('#platformFilter').val(), 'i');
            var rex4 = new RegExp($('#languageFilter').val(), 'i');
            var rex5 = new RegExp($('#availabilityFilter').val());
            $('.searchable tr').hide();
            $('.searchable tr').filter(function () {
                return rex.test($(this).text()) && rex2.test($(this).text()) && rex3.test($(this).text()) && rex4.test($(this).text()) && rex5.test($(this).text());
            }).show();

        })

        $('#languageFilter').change(function () {
            var rex = new RegExp($(this).val(), 'i');
            var rex2 = new RegExp($('#filter').val(), 'i');
            var rex3 = new RegExp($('#platformFilter').val(), 'i');
            var rex4 = new RegExp($('#regionFilter').val(), 'i');
            var rex5 = new RegExp($('#availabilityFilter').val());
            $('.searchable tr').hide();
            $('.searchable tr').filter(function () {
                return rex.test($(this).text()) && rex2.test($(this).text()) && rex3.test($(this).text()) && rex4.test($(this).text()) && rex5.test($(this).text());
            }).show();

        })

        $('#availabilityFilter').change(function () {
            var rex = new RegExp($(this).val());
            var rex2 = new RegExp($('#filter').val(), 'i');
            var rex3 = new RegExp($('#platformFilter').val(), 'i');
            var rex4 = new RegExp($('#regionFilter').val(), 'i');
            var rex5 = new RegExp($('#languageFilter').val(), 'i');
            $('.searchable tr').hide();
            $('.searchable tr').filter(function () {
                return rex.test($(this).text()) && rex2.test($(this).text()) && rex3.test($(this).text()) && rex4.test($(this).text()) && rex5.test($(this).text());
            }).show();

        })
    }(jQuery));

});	