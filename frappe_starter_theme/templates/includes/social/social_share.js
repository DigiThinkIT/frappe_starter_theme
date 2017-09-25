frappe.ready(function() {
	$('.share-buttons a.pop').click(function(e) {
		var pop_width = 500;
		var pop_height = 500;
		var left = ($(window).width() - pop_width) / 2;
		var top = ($(window).height() - pop_height) / 2;
		var win = window.open($(this).attr("href"), "Share Article", 'left='+left+',top='+top+',width=500,height=500,toolbar=1,resizable=0');
		win.focus();
		e.preventDefault();
		e.stopPropagation();
		return false;
	})
});
