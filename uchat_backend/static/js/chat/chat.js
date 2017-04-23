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
			$('#chat1').children().remove();
			var $first_dom = $('.' + settings.friends).children('.friend-detail').first();
			// console.log($first_dom);
			// Change heading
			var name = getName($first_dom);
			$('#friend-name-heading').text(name);

			// Load previous chat
			// loadPreviousChat($first_dom, channel);

			
			var channel = getChannel($first_dom);
			loadPreviousChat($first_dom, channel);
			// console.log(channel);
			$(document).on('click', '.friend-detail', onClick);
			// connect every channel to socket
			$('.' + settings.friends).children('.friend-detail').each(function() {
				$this = $(this);
				// $this.on("click", onClick);
				
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
			$('#chat1').children().remove();

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
			// console.log(settings.chatsock);

			if (settings.chatsock[friend]) {
				connectWebSocket(settings.chatsock[friend]);	
			} else {
				var chatsock = createWebSocket(channel);
				settings.chatsock[friend] = chatsock;
				console.log(chatsock);
				connectWebSocket(settings.chatsock[friend]);
			}
			

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
			var $chats = $('#chat1');
			for (var chat of chats) {			
				var $chat = individualChat(chat);
				$chats.append($chat);
			}

			$('#chat1').scrollTop($('#chat1')[0].scrollHeight);

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
			var flag = 0;
			console.log(chat.timestamp);
			var datetime = getDateTime(chat.timestamp);

			var pre_date = $('.date-msg').last().text();
			
			if (pre_date === datetime.date) {
				// console.log('Here', datetime.date, pre_date);
				flag = 1;
			} else {
				flag = 0;
			}
			t_p_date = datetime.date;
			// console.log('Flag check', flag, flag ? datetime.time : '');
			// console.log(flag, pre_date, datetime.date);
			var source   = $("#message-template").html();
			var template = Handlebars.compile(source);
			var context = {
				message: chat.message,
				out: out,
				date: datetime.date,
				time: datetime.time,
				hidden:  flag ? 'hidden' : '',
			};
			var $ele = template(context); 

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
					// console.log(message.handle, loggedUser, activeFriend);
					if (data.handle == loggedUser || data.handle == activeFriend) {
						// console.log('I am inside');
						renderChat([data]);
					} else {
						var handle = data.handle;
						// Grab the span for this and remove hidden class and increase counter of unread message
						var counter = parseInt($('#' + handle).text());
						// console.log(handle, counter, $('#' + handle).text());
						counter += 1;
						
						var target = $('#' + handle).parent();
						// var target = $('#test6').parent();
						var $first_dom = $('.' + settings.friends).children('.friend-detail').first();
						console.log(target, target.position().top - $first_dom.position().top);
						target.animate({
							top: -(target.position().top - $first_dom.position().top),
							 opacity: 0.25,
						}, 'fast', function() {
							// target.insertBefore($first_dom);
							$('.friends-list strong').after(target[0]);
							$('#' + handle).text(counter).removeClass('hidden');
							console.log(target);
							target.css('opacity', 1);
							target.css('top', 0);
						})
						// moveUp(target);
					}
				} else {
					// console.log('connected', settings.chatsock.url);
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

		// Animation as per messages come
		// function css(element, property, value) {
		// 	element.style.transitionDuration = '0ms';
		// 	element.style[property] = value;
		// }

		function animate(element, property, value, duration, callback) {
			duration = duration == null ? 400 : parseFloat(duration);
			element.style.transitionDuration = duration + 'ms';
			element.offsetLeft;
			element.style[property] = value;
			duration && callback && setTimeout(function () {
			callback(element);
			}, duration);
		}

		function moveUp(element) {
			var curr = element.parentNode;
			var prev = $('.' + settings.friends).children('.friend-detail').first();

			console.log(curr, prev);
			if (!prev) return false;

			animate(curr, 'top', -prev.offsetHeight + 'px', null, function () {
				curr.parentNode.insertBefore(curr, prev);
				css(curr, 'top', 0);
				css(prev, 'top', 0);
			});
			// animate(prev, 'top', curr.offsetHeight + 'px', null, function () {
			// curr.parentNode.insertBefore(curr, prev);
			// css(curr, 'top', 0);
			// css(prev, 'top', 0);
			// });
		}
	}
}(jQuery));