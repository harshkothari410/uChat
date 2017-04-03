$(function(){
	var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
	$('#chat').scrollTop($('#chat')[0].scrollHeight);


    // var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat/47716bb0-5f9b-4676-9474-706cc95dc801");
    
    chatsock.onmessage = function(message) {
        // alert(message.data);
        console.log(message.data);
        if (message.data != 'hello') {
        	// console.log(message.data);
	        var data = JSON.parse(message.data);


	        var chat = $("#chat")
	        var ele = $('<div></div>').addClass('msg');

	        var $div = $('<div></div>').addClass('bubble bubble-text has-author');
	        var $innerDiv = $('<div></div>').addClass('message-text');

	        if (data.handle == $('#user-info-username').text()) {
	        	$innerDiv.addClass('message-out');
	        }
	        var $span = $('<span></span>').addClass('emojitext selectable-text').text(data.handle + ' - ' + data.message);
	        
	        $innerDiv.append($span);

	        $div.append($innerDiv);

	        ele.append($div);

	        
	        chat.append(ele);
	        $('#chat').scrollTop($('#chat')[0].scrollHeight);
	    }
    };

    // chatsock.onconnect(e) {
    //     console.log(e.data);
    // }

    $("#chatsend").on("click", function(event) {
    	event.preventDefault();
        var message = {
            handle: $('#user-info-username').text(),
            message: $('#chatmessage').val(),
        }
        console.log(JSON.stringify(message));
        chatsock.send(JSON.stringify(message));
        $("#chatmessage").val('').focus();
        return false;
    });
})