/* seachbar.js 
 * 
 * JS file for searchbar
 * Author : Harsh Kothari, Vidit Desai
 */
$(function(){

//typeahead

	// var friends=['Vidit','Veelmay','Varsh','Anirudh','Gaurav'];
	t_friends = [];
	// var friends = [{
	// 	'name': 'vidit',
	// 	'username': 'vidit124'
	// }, {
	// 	'name': 'vidit',
	// 	'username': 'v222'
	// }]
	groups=['2H','1C','Goa','Washington','Vegas Trip','CS552', 'Viddddii'];

	$('.friends-list').children('.friend-detail').each(function() {
		$this = $(this);
		var name = $this.children('.socket-chat').attr('friend-name');
		var username = $this.children('.socket-chat').attr('friend');
		window.t_friends.push({
			name: name,
			username, username
		})

		bindSearch();
	});
	
	
	$('.friends-group-search .typeahead').typeahead({
		highlight:true,
		hint: true,
		minLength: 1,
	},
	{
		name:'myfriends',
		displayKey: 'name',
		source:typeaheadFriends,
		templates:{
		header:'<h4>Friends</h4>'
			}
	},
	{
		name:'mygroups',
		// display:'name',
		source:typeaheadGroups,
		templates:{
			header:'<h4>Groups</h4>'
		}
	});

	$('.typeahead').on('typeahead:autocompleted', function(e, datum) {
		if (datum.username) {
			console.log(datum.username);
			var target = $('#' + datum.username).parent();
			target.trigger('click');
			$('.typeahead').typeahead('val','');
		}
	});

	$('.typeahead').on('typeahead:selected', function(e, datum) {
		if (datum.username) {
			console.log(datum.username);
			var target = $('#' + datum.username).parent();
			target.trigger('click');
			$('.typeahead').typeahead('val','');
		}
	});
})

var bindSearch = function() {
	typeaheadFriends =new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		local: window.t_friends
	});

	typeaheadGroups =new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.whitespace,
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		local:groups
	});
}