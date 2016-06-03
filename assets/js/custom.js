// Mobile Menu
function DropDown(el) {
	this.dd = el;
	this.initEvents();
}

DropDown.prototype = {
	initEvents : function() {
		var obj = this;

		obj.dd.on('click', function(event){
			jQuery(this).toggleClass('active');
			event.stopPropagation();
		});	
	}
}

jQuery(function($) {
	var dd = new DropDown( jQuery('#dd') );

	$(document).click(function() {
		// all dropdowns
		$('.mobile-menu').removeClass('active');
	});

	$( "#faq" ).accordion({
		active: false,
		collapsible: true,
		heightStyle: "content"
	});


});

jQuery(window).load(function(){
	jQuery('.testimonials').flexslider({
		slideshowSpeed: 15000,
		animation: "slide"
	});

	jQuery('.partner-logos').flexslider({
		animation: "slide",
		controlNav: false,
		itemWidth: 350,
		minItems: 5,
		maxItems: 5,
		animationLoop: false
	});
});

/*
jQuery(document).ready(function() {
	jQuery('.graph-overlay').addClass("hidden").viewportChecker({
		classToAdd: 'visible animated fadeIn',
		offset: 200
	});
});
*/

jQuery(window).scroll( function(){
	jQuery('.graph-overlay:in-viewport').animate({
		opacity:1
	},4000);	
});

/*
jQuery(window).scroll( function(){
	jQuery('.line').animate({
			bottom:0
		},8000, function(){
		
		
		jQuery('.customer-logo').animate({
			opacity:1
		},1000);
	});

});
*/
