$(function(){
	Handlebars.registerHelper('breaklines', function(text) {
		    text = Handlebars.Utils.escapeExpression(text);
		    text = text.replace(/(\r\n|\n|\r)/gm, '<br>');
		    return new Handlebars.SafeString(text);
		});
	// Image Icon based on Name
	data = { height : 50, width : 50, fontsize : 10};

	$('.chat-container').chat();
	// $('.bot-container').chatbot();
	$('.initial-image').initial();

})

