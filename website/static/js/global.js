$(document).ready(function(){
/*$(":input").bind('keyup change click', function (e) {
    if (! $(this).data("previousValue") || 
           $(this).data("previousValue") != $(this).val()
       )
   {
        
        $(this).data("previousValue", $(this).val());
   }
        
});


$(":input").each(function () {
    $(this).data("previousValue", $(this).val());
});*/

  var hash = window.location.hash;
  hash && $('ul.nav a[href="' + hash + '"]').tab('show');

  $('.nav-tabs a').click(function (e) {
    $(this).tab('show');
    var scrollmem = $('body').scrollTop();
    window.location.hash = this.hash;
    $('html,body').scrollTop(scrollmem);
    
  });

});