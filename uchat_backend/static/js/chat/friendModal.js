
//Hides Label and Submit Button
$('#sidebar-add-friend').click(function(){
			$('#searchFriendResult').hide();
			$('#modalFriendsubmit').hide();
})

// Search Friend Function
$('#modalFriendSearch').click(function(){

			$.ajax({
				url:"http://barttiming.herokuapp.com/v1/subjects/BART.12th",
				dataType:"jsonp",
				crossDomain:true, 
				succes:function(result){
					// alert("Hello");
					$('#searchFriendResult').show();
					$('#modalFriendsubmit').show();
					$('#searchFriendResult').text($('#friend-name').val());
				},
				error:function(result){
					// alert(result);
					$('#searchFriendResult').show();
					$('#modalFriendsubmit').show();
					$('#searchFriendResult').text($('#friend-name').val());
				}
			});
})


// Submit Friend
$('#modalFriendsubmit').click(function(){
			
			var name = $('#friend-name').val();
			var $div = $('<div>').addClass('sidebar-item-icon');
			var $span = $('<span>').addClass('glyphicon glyphicon-user');
			var $dom = $('<div>').addClass('sidebar-item').addClass('friends-item');

			$div.append($span);
			$dom.append($div);
			var $div = $('<div>').addClass('sidebar-item-title').text(name);
			$dom.append($div);
			$('.friends-list').prepend($dom);
			
			var fvis = $('.friends-item');
			if(fvis.length>5){
				// console.log("Hello");
				for(i=5;i<fvis.length;i++){
					$(fvis[i]).hide();
				}
			}


})