var loading = false;

$(document).ready(function(){ 
	updateContainer("/static/main.html", false);
});

function updateContainer(path, animated) {
	if(loading) 
		return;
	loading = true;

	var speed = (typeof(animated) === "undefined" || animated) ? 250 : 0;
	$(".container").animate({opacity:0}, speed, function() {
		$.ajax({
			url : path, 
			success: function(data) {
				$(".container").showHtml(data, speed, function() {
				  	loading = false;
			  		$(".container").animate({opacity:1}, speed);
				});
			}, 
			async: false
		});
	});
}

(function($) {
   $.fn.showHtml = function(html, speed, callback) {
      return this.each(function() {
         var el = $(this);
         var finish = {width: this.style.width, height: this.style.height};
         var cur = {width: el.width()+'px', height: el.height()+'px'};
         el.html(html);
         var next = {width: el.width()+'px', height: el.height()+'px'};
         el .css(cur) 
            .animate(next, speed, function() {
               el.css(finish); 
               if ( $.isFunction(callback) ) callback();
            });
      });
   };
})(jQuery);