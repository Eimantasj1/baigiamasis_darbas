var lastScrollTop = 0;

window.addEventListener("scroll", function() {
  var st = window.pageYOffset || document.documentElement.scrollTop;
  
  if (st > lastScrollTop){
    document.querySelector('.footer').style.bottom = "-100px";
  } else {
    document.querySelector('.footer').style.bottom = "0";
  }

  lastScrollTop = st <= 0 ? 0 : st;
});