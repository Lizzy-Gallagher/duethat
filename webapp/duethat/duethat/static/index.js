var base_url = "https://api.projectoxford.ai/luis/v1/application?id=a500a19e-f7ab-4078-9f6c-9b6b8ee3bbeb&subscription-key=598c92029bc24dff8b713c669d774773&q="


var classify = function() {
	var text = document.getElementById("query").value;
	console.log(text);

	var full_url = base_url + text;
	$.getJSON(full_url, function(data) {
		// do something
		readJSON(data);
		console.log("finished");
	});
}

var readJSON = function(data) {
	var json = JSON.parse(data);
	console.log(json["intents"][0]["intent"]);
	console.log(json["entities"][0]["entity"]);
}