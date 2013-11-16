var audio;
function beginSongWithSource(source) {
	if (audio) {
		audio.pause();
	}
    audio = new Audio();
    audio.setAttribute("src",source);
    audio.play();
}