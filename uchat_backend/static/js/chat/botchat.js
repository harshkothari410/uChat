$(function($){

	$.fn.chatbot = function(options) {
		var settings = $.extend({
			'friends' : 'friends-list',
			'groups' : 'groups-item',
			'base_url' : '/api/v1/',
			'chatsock' : {},
			'runningSock' : null
		})

		// init function for rendering first chat
		this.init = function() {
			

			connectWebSocket(settings.chatsock['bot']);
			settings.runningSock = settings.chatsock['bot'];
		}

		// init function call
		this.init();


		// Listen message on indvidual channel
		function connectWebSocket(chatsock) {
			chatsock.onmessage = function(message) {
				if (message.data != 'hello') {

					// console.log(message, settings.chatsock.url);
					var data = JSON.parse(message.data);
					// console.log(data);
					// var activeFriend = getFriend($('.active'));
					var loggedUser = $('#user-info-username').text();
					// console.log(message.handle, loggedUser, activeFriend);
					// if (data.handle == loggedUser || data.handle == activeFriend) {
						// console.log('I am inside');
						renderChat([data]);
					// } else {
						// var handle = data.handle;
						// // Grab the span for this and remove hidden class and increase counter of unread message
						// var counter = parseInt($('#' + handle).text());
						// // console.log(handle, counter, $('#' + handle).text());
						// counter += 1;
						
						// var target = $('#' + handle).parent();
						// // var target = $('#test6').parent();
						// var $first_dom = $('.' + settings.friends).children('.friend-detail').first();
						// console.log(target, target.position().top - $first_dom.position().top);
						// target.animate({
						// 	top: -(target.position().top - $first_dom.position().top),
						// 	 opacity: 0.25,
						// }, 'fast', function() {
						// 	// target.insertBefore($first_dom);
						// 	$('.friends-list strong').after(target[0]);
						// 	$('#' + handle).text(counter).removeClass('hidden');
						// 	console.log(target);
						// 	target.css('opacity', 1);
						// 	target.css('top', 0);
						// })
						// moveUp(target);
					// }
				} else {
					console.log('connected', settings.chatsock.url);
				}
			}
		}

		function renderChat(chats) {
			var $chats = $('#chat2');
			for (var chat of chats) {			
				var $chat = individualChat(chat);
				$chats.append($chat);
			}

			$('#chat2').scrollTop($('#chat2')[0].scrollHeight);

			$('.initial-image').initial();
		}

		// individual chat template
		// @fix me - Change as per the new design
		function individualChat(chat) {
			// Using Handlebars template rendering engine
			var out = '';
			if (chat.handle == $('#user-info-username').text()) {
				out = 'message-out';
			}
			// var t_p_date = '';
			// var flag = 0;
			// console.log(chat.timestamp);
			// var datetime = getDateTime(chat.timestamp);

			// var pre_date = $('.date-msg').last().text();
			
			// if (pre_date === datetime.date) {
			// 	// console.log('Here', datetime.date, pre_date);
			// 	flag = 1;
			// } else {
			// 	flag = 0;
			// }
			// t_p_date = datetime.date;
			// console.log('Flag check', flag, flag ? datetime.time : '');
			// console.log(flag, pre_date, datetime.date);
			var source   = $("#message-template-bot").html();
			var template = Handlebars.compile(source);
			var context = {
				message: chat.message,
				out: out,
				user: chat.handle,
				// date: datetime.date,
				// time: datetime.time,
				// hidden:  flag ? 'hidden' : '',
			};
			var $ele = template(context); 

			return $ele;
		}

		// Send message to channel
		// @fix me to make more general function
		// settings.chatsock = chatsock;
		$("#chatsendbot").on("click", function(event) {
			// console.log('I am fucking here');
			event.preventDefault();
			var message = {
				handle: $('#user-info-username').text(),
				message: $('#chatmessagebot').val(),
			}
			console.log(JSON.stringify(message));
			renderChat([message]);
			settings.runningSock.send(JSON.stringify(message));
			$("#chatmessagebot").val('').focus();
			return false;
		});

		$('#chatmessagebot').on('click', function(event) {
			console.log('I am in here');
			if (settings.chatsock['bot']) {
				console.log(settings.chatsock['bot'])
				connectWebSocket(settings.chatsock['bot']);	
				settings.runningSock = settings.chatsock[friend];
			}
		})

		// connect to websocket
		function createWebSocket(channel) {
			var url = getWebSocketURL(channel);
			var chatsock = new ReconnectingWebSocket(url);
			return chatsock;
		}

		// get URL for channel to connect websocket
		function getWebSocketURL(channel) {
			var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
			return ws_scheme + '://' + window.location.host + "/chat/" + channel;
		}

		// find the channel based on friend or group
		function getChannel() {
			return $('#chat2').attr('channel');
		}
		
		// get timestamp from date string
		function getDateTime(timestamp) {
			var rdt = {};

			var dt = new Date(timestamp);
			console.log(dt);
			var d = dt.getMonth()+1 + '/' + dt.getDate() + '/' + dt.getFullYear();
			var hour = dt.getHours();
			var minutes = dt.getMinutes();
			var ampm = 'AM';
			// Check for AM PM
			if (parseInt(hour) > 12) {
				hour = parseInt(hour) - 12;
				ampm = 'PM';
			}
			var t = hour + ':' + minutes + ' ' + ampm;
			rdt['date'] = d;
			rdt['time'] = t;
			return rdt;
		}


	}
}(jQuery));