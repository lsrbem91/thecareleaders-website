/* YouTube videos load only when someone presses play, so no third-party cookies are set before that. */
document.addEventListener('click', function (e) {
  var b = e.target.closest('.yt-play'); if (!b) return;
  var ph = b.closest('.yt-ph'), f = document.createElement('iframe');
  f.src = 'https://www.youtube-nocookie.com/embed/' + ph.getAttribute('data-yt') + '?autoplay=1';
  f.title = ph.getAttribute('data-title');
  f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture'; f.allowFullscreen = true;
  ph.replaceWith(f);
});
