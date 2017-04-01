$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    // var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat/47716bb0-5f9b-4676-9474-706cc95dc801");
    
    chatsock.onmessage = function(message) {
        // alert(message.data);
        var data = JSON.parse(message.data);
        console.log(data);
        var chat = $("#chat")
        var ele = $('<tr></tr>')

        ele.append(
            $("<td></td>").text(data.timestamp)
        )
        ele.append(
            $("<td></td>").text(data.handle)
        )
        ele.append(
            $("<td></td>").text(data.message)
        )
        
        chat.append(ele)
    };

    // chatsock.onconnect(e) {
    //     console.log(e.data);
    // }

    $("#chatform").on("submit", function(event) {
        var message = {
            handle: $('#handle').val(),
            message: $('#message').val(),
        }
        console.log(JSON.stringify(message));
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
    });
});