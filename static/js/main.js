function addSong(song) {
  var table = $(".uploadTable tbody");
  var progress = '<div style="vertical-align:middle;" class="progress progress-striped active" role="progressbar" aria-valuemin="0" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="progress-bar progress-bar-success" style="width:0%;"></div></div>';
  var row = '<tr><td>' + song.title + '</td><td>' + progress + '</td><td>' + song.length + '</td></tr>';
  table.append(row);
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

String.prototype.toHHMMSS = function () {
  var sec_num = parseInt(this, 10); // don't forget the second parm
  var hours   = Math.floor(sec_num / 3600);
  var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
  var seconds = sec_num - (hours * 3600) - (minutes * 60);

  if (hours   < 10) {hours   = "0"+hours;}
  if (minutes < 10) {minutes = "0"+minutes;}
  if (seconds < 10) {seconds = "0"+seconds;}
  var time    = hours+':'+minutes+':'+seconds;
  return time;
}
