// Filter chips and slider controls for the work listings
document.querySelectorAll('[data-filter-scope]').forEach(function(scope){
  var chips=scope.querySelectorAll('.chip');
  var cards=scope.querySelectorAll('.work-card');
  chips.forEach(function(chip){
    chip.addEventListener('click',function(){
      var f=chip.getAttribute('data-f');
      chips.forEach(function(c){var on=c===chip;c.classList.toggle('on',on);c.setAttribute('aria-pressed',on?'true':'false');});
      cards.forEach(function(card){
        var cats=(card.getAttribute('data-cats')||'').split(' ');
        card.hidden=!(f==='all'||cats.indexOf(f)>-1);
      });
      var sl=scope.querySelector('.slider'); if(sl) sl.scrollTo({left:0,behavior:'smooth'});
    });
  });
  var sl=scope.querySelector('.slider');
  if(sl){
    var step=function(){var c=sl.querySelector('.work-card:not([hidden])');return c?c.getBoundingClientRect().width+20:320;};
    var p=scope.querySelector('.sl-prev'),n=scope.querySelector('.sl-next');
    if(p)p.addEventListener('click',function(){sl.scrollBy({left:-step(),behavior:'smooth'});});
    if(n)n.addEventListener('click',function(){sl.scrollBy({left:step(),behavior:'smooth'});});
  }
});

// Tabs: the "What do you need to change?" selector
document.querySelectorAll('[data-tabs]').forEach(function(box){
  var tabs=[].slice.call(box.querySelectorAll('[role="tab"]'));
  function show(t){tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on?'true':'false');x.tabIndex=on?0:-1;var p=document.getElementById(x.getAttribute('aria-controls'));if(p)p.hidden=!on;});}
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){show(t);});
    t.addEventListener('keydown',function(e){var k=e.key,n=null;if(k==='ArrowDown'||k==='ArrowRight')n=tabs[(i+1)%tabs.length];if(k==='ArrowUp'||k==='ArrowLeft')n=tabs[(i-1+tabs.length)%tabs.length];if(n){e.preventDefault();show(n);n.focus();}});
  });
});
