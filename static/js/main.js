var songs = [
	{
		title: "Fun",
		length: "2:20"
	},
	{
		title:"Hello",
		length: "5:10"
	},
	{
		title:"Rolling in the deep",
		length: "10:10"
	},
]

function updateTable () {
	var table = $(".uploadTable tbody");
	var entries = [];
	for (var i = 0; i < songs.length; i++) {
		var row = "<tr><td>" + (i+1) + "</td><td>" + songs[i].title + "</td><td>" + songs[i].length + "</td></tr>";
		entries.push(row);
	}
	table.html(entries);
}

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