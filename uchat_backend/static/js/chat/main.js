$(function(){

	// Image Icon based on Name
	data = { height : 50, width : 50, fontsize : 10};
	$('.initial-image').initial();

	//typeahead

	var friends=['Vidit','Neelmay','Harsh','Anirudh','Gaurav'];
	var groups=['2H','1C','Goa','Washington','Vegas Trip','CS552', 'Viddddii'];

	var typeaheadFriends =new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.whitespace,
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		local: friends
	});

	var typeaheadGroups =new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.whitespace,
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		local:groups
	});

			// console.log(typeaheadFriends);
	$('.friends-group-search .typeahead').typeahead({
		highlight:true,
		hint: true,
		minLength: 1,
	},
	{
		name:'myfriends',
		// display:'name',
		source:typeaheadFriends,
		templates:{
		header:'<h3>Your Friends</hr>'
			}
	},
	{
		name:'mygroups',
		// display:'name',
		source:typeaheadGroups,
		templates:{
			header:'<h3>Your Groups</hr>'
		}
	});

})

