$(function($){

	$.fn.chat = function(options) {
		var settings = $.extend({
			'friends' : 'friends-list',
			'groups' : 'groups-item',
			'base_url' : '/api/v1/',
			'chatsock' : {},
			'runningSock' : null
		})

		// init function for rendering first chat
		this.init = function() {
			$('#chat').children().remove();
			var $first_dom = $('.' + settings.friends).children().first();

			// Change heading
			var name = getName($first_dom);
			$('#friend-name-heading').text(name);

			// Load previous chat
			// loadPreviousChat($first_dom, channel);

			
			var channel = getChannel($first_dom);
			loadPreviousChat($first_dom, channel);

			// connect every channel to socket
			$('.' + settings.friends).children().each(function() {
				$this = $(this);
				$this.on("click", onClick);
				var channel = getChannel($this);
				var chatsock = createWebSocket(channel);
				// settings.chatsock = chatsock;
				var friend = getFriend($this);
				settings.chatsock[friend] = chatsock;
				connectWebSocket(settings.chatsock[friend]);
			});

			// Connect first dom to channel
			var friend = getFriend($first_dom);
			$first_dom.addClass('active');
			// connectWebSocket(settings.chatsock[friend]);
			settings.runningSock = settings.chatsock[friend];
		}

		// init function call
		this.init();


		// onClick event listner
		function onClick() {
			$('#chat').children().remove();

			$('.active').each(function(){
				$(this).removeClass('active');
			});

			// $('#' + handle).value(0).addClass('hidden');

			$this = $(this);
			$this.addClass('active');
			var channel = getChannel($this);
			var username = getUserName($this);
			var friend = getFriend($this);
			var name = getName($this);
			console.log(settings.chatsock);
			connectWebSocket(settings.chatsock[friend]);

			// Make chat count 0
			$('#' + username).val(0).addClass('hidden');

			settings.runningSock = settings.chatsock[friend];
			// Change heading
			$('#friend-name-heading').text(name);

			// Load previous chat
			loadPreviousChat($this, channel);
		}

		// load previos chat
		function loadPreviousChat(channel) {
			// Change URL in future group and friend URL
			var url = getChatURL(channel);
			$.ajax({
				url: url,
				type: 'GET',
				dataType:"json",
			})
			.done(function(data) {
				renderChat(data);
			})
			.error(function(data) {
				console.log(data);
			})
		}

		// function for redering chat
		function renderChat(chats) {
			var $chats = $('#chat');
			for (var chat of chats) {			
				var $chat = individualChat(chat);
				$chats.append($chat);
			}

			$('#chat').scrollTop($('#chat')[0].scrollHeight);
		}

		// individual chat template
		// @fix me - Change as per the new design
		function individualChat(chat) {
			// console.log(chat);
			var $ele = $('<div></div>').addClass('msg');
			var $div = $('<div></div>').addClass('bubble bubble-text has-author');
			var $innerDiv = $('<div></div>').addClass('message-text');

			if (chat.handle == $('#user-info-username').text()) {
				$innerDiv.addClass('message-out');
			}

			var $span = $('<span></span>').addClass('emojitext selectable-text').text(chat.handle + ' - ' + chat.message);
			$innerDiv.append($span);
			$div.append($innerDiv);
			$ele.append($div);

			return $ele;
		}

		// Listen message on indvidual channel
		function connectWebSocket(chatsock) {
			chatsock.onmessage = function(message) {
				if (message.data != 'hello') {

					// console.log(message, settings.chatsock.url);
					var data = JSON.parse(message.data);
					// console.log(data);
					var activeFriend = getFriend($('.active'));
					var loggedUser = $('#user-info-username').text();
					console.log(message.handle, loggedUser, activeFriend);
					if (data.handle == loggedUser || data.handle == activeFriend) {
						// console.log('I am inside');
						renderChat([data]);
					} else {
						var handle = data.handle;
						// Grab the span for this and remove hidden class and increase counter of unread message
						var counter = parseInt($('#' + handle).text());
						// console.log(handle, counter, $('#' + handle).text());
						counter += 1;
						$('#' + handle).text(counter).removeClass('hidden');
					}
				} else {
					console.log('connected', settings.chatsock.url);
				}
			}
		}

		// Send message to channel
		// @fix me to make more general function
		// settings.chatsock = chatsock;
		$("#chatsend").on("click", function(event) {
			event.preventDefault();
			var message = {
				handle: $('#user-info-username').text(),
				message: $('#chatmessage').val(),
			}
			console.log(JSON.stringify(message));
			settings.runningSock.send(JSON.stringify(message));
			$("#chatmessage").val('').focus();
			return false;
		});

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

		// find chat URL
		function getChatURL(dom, channel) {
			creator = getCreator(dom);
			friend = getFriend(dom);
			return settings.base_url + 'users/' + creator + '/friends/' + friend + '/chats/'; 
		}

		// find name
		function getName(dom) {
			return dom.children('.socket-chat').attr('friend-name');
		}

		// find creator
		function getCreator(dom) {
			return dom.children('.socket-chat').attr('creator');
		}

		// find friend
		function getFriend(dom) {
			return dom.children('.socket-chat').attr('friend');
		}

		// find username
		function getUserName(dom) {
			return dom.children('.socket-chat').attr('user-name');
		}

		// find the channel based on friend or group
		function getChannel(dom) {
			return dom.children('.socket-chat').attr('chat-id');
		}
	}
}(jQuery));