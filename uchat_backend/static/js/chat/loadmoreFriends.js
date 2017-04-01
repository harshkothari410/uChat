$('#loadMoreFriends').click(function(){
	var fvis = $('.friends-item');
	for(var i =0;i<fvis.length;i++){
		$(fvis[i]).show();
		}
	$('#loadMoreFriends').hide();

})
