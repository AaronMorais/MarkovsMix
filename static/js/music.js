var currentAudioIndex = 0; 
var songSources = ["music/sng1.ogg", "music/sng2.ogg", "music/1.mp3", "music/2.mp3"];
var audioObjects = [];
var playing = false;

function beginMusic() {
  for (var i=0; i<songSources.length; i++) {
	  var audio = new Audio();
	  audio.setAttribute("src",songSources[i]);
  	  audio.addEventListener("ended", function changeAudio() {
  	  	playNextAudioSource();
	  });
	  audioObjects.push(audio);
  }

  var play = document.getElementById('play')
  play.addEventListener('click', function() {
  	if (playing) {
	  	audioObjects[currentAudioIndex].pause();
  	} else {
	  	audioObjects[currentAudioIndex].play();
  	}
	playing = !playing;
  });
}

function playNextAudioSource() {
	currentAudioIndex++;
	currentAudioIndex %= audioObjects.length;
	audioObjects[currentAudioIndex].play();
}