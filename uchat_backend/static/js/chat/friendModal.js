
//Hides Label and Submit Button
$('#sidebar-add-friend').click(function(){
	$('#searchFriendResult').hide();
	// $('#modalFriendsubmit').hide();
})

// Search Friend Function
$('#modalFriendSearch').click(function(){

	var base_friend_find_url = '/api/v1/users/';

	var username = $('#friend-name').val();
	var url = base_friend_find_url + username;
	$.ajax({
		url: url,
		type: 'GET',
		dataType:"json",
		success:function(data){
			console.log(data);
			$('#searchFriendResult').show();
			$('.addfriendbutton').show();
			// $('#modalFriendsubmit').show();
			$('#searchFriendResult > .name').text(data.first_name + ' ' + data.last_name).attr('val', data.username);
		},
		error:function(data){
			// console.log(data.statusText);
			$('#searchFriendResult').show();
			$('.addfriendbutton').hide();
			$('#searchFriendResult > .name').text('User not Found. Try again !');
		}
	});
})


// Submit Friend
$('#modalFriendsubmit').click(function(){
			
	var name = $('#friend-name').val();
	
	// Ajax POST request to add friend
	var base_friend_find_url = '/api/v1/users/';

	var username = $('#user-info-username').text();
	var url = base_friend_find_url + username + '/friends/';
	data = {
		'username': $('#searchFriendResult > .name').attr('val')
	};

	var csrftoken = getCookie('csrftoken');
	console.log(url);
	$.ajax({
		url:url,
		type: 'POST',
		data: data,
		dataType: 'json',
		headers: {
			'X-CSRFToken' : csrftoken
		},
		success: function(data){
			
			var source   = $("#friend-template").html();
			var template = Handlebars.compile(source);
			var context = {
				friend_name: data.friend.first_name + ' ' + data.friend.last_name,
				friend_username: data.friend.username,
				chatid: data.room.label,
				creator_username: username,
				hidden: 'hidden',
			};
			var $ele = template(context); 
			$('.friends-list strong').after($ele);

			var fvis = $('.friends-item');
			if(fvis.length>5){
				// console.log("Hello");
				for(i=5;i<fvis.length;i++){
					$(fvis[i]).hide();
				}
			}

			var name = data.friend.first_name + ' ' + data.friend.last_name;
			var username = data.friend.username;
			window.t_friends.push({
				name: name,
				username, username
			})

			bindSearch();
			$('.friends-list').children('.friend-detail').first().trigger('click');
		},
		error: function(data) {
			console.log(data);
			$('#searchFriendResult').text('Failed try again!');
		}
	});

	

	// $ele.trigger("click");
	// $('.friends-list').children('.friend-detail').first()[0].trigger('click');

})


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
