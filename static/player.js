document.addEventListener('DOMContentLoaded', () => {
  const video = document.getElementById('video-player');
  const playPauseBtn = document.getElementById('play-pause');
  const progress = document.getElementById('progress');
  const fullscreenBtn = document.getElementById('fullscreen');

  playPauseBtn.addEventListener('click', () => {
    if (video.paused) {
      video.play();
      playPauseBtn.textContent = '⏸';
    } else {
      video.pause();
      playPauseBtn.textContent = '▶';
    }
  });

  video.addEventListener('timeupdate', () => {
    progress.value = (video.currentTime / video.duration) * 100;
  });

  progress.addEventListener('input', () => {
    video.currentTime = (progress.value / 100) * video.duration;
  });

  fullscreenBtn.addEventListener('click', () => {
    if (!document.fullscreenElement) {
      video.requestFullscreen();
    } else {
      document.exitFullscreen();
    }
  });
});

video.addEventListener('play', () => {
  if (video.requestFullscreen) {
    video.requestFullscreen();
  } else if (video.webkitRequestFullscreen) { /* Safari */
    video.webkitRequestFullscreen();
  } else if (video.msRequestFullscreen) { /* IE11 */
    video.msRequestFullscreen();
  }
});
