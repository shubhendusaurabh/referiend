$(document).ready(function(){
  $('.task').click(function(){
    var image = $(this).find('img'),
    loading = $(this).parent().find('.loading');

    $.ajax({
      url: '/admin/charts/chart/scrap-songs/',
      beforeSend: function(){
        image.hide();
        loading.show();
      },
      statusCode: {
        200: function() {
          loading.hide();
          image.attr('src', '/static/img/success.png');
          image.show();
        },
        404: function() {
          loading.hide();
          image.attr('src', '/static/img/error.png');
          image.show();
        },
        500: function() {
          loading.hide();
          image.attr('src', '/static/img/error.png');
          image.show();
        }
      }
    });
  });
});

