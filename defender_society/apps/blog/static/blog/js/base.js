//bootstrap4 tooltips
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});
//back to the top
$(window).scroll(function(){
    $('#to-top').hide();
    if ($(window).scrollTop()>=600){
        $('#to-top').show();
    };
});
$("#to-top").click(function () {
        var speed=400;//The speed of sliding
        $('body,html').animate({ scrollTop: 0 }, speed);
        return false;
 });
//Mouse over the title bar to show the drop-down
$(function() {
var $dropdownLi = $('ul.navbar-nav> li.dropdown');
$dropdownLi.mouseover(function() {
$(this).addClass('show');
$(this).children('a.dropdown-toggle').attr('aria-expanded','true');
$(this).children('div.dropdown-menu').addClass('show')
}).mouseout(function() {
$(this).removeClass('show');
$(this).children('a.dropdown-toggle').attr('aria-expanded','false');
$(this).children('div.dropdown-menu').removeClass('show')
})
});
//The anchor point moves smoothly to the specified position
function TOC_FUN(A) {
$(A).click(function() {
$(A).css("color", "#0099ff");
$(this).css("color", "red");
$('html, body').animate({
scrollTop: $($.attr(this,'href')).offset().top-55
}, 500);
return false
})
}
$(TOC_FUN('.toc a,.to-com'));