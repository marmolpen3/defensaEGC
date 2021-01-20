

$.getJSON('static/js/lang.json', function(json){
  $('.translate').click(function(){
    let lang = $(this).attr('id');
    $('.lang').each(function(index, element){
      element.innerText=json[lang][element.id];
     // $(this).text(json[lang][$(this).attr('id')]);
    });
  });

});//Get json AJAX