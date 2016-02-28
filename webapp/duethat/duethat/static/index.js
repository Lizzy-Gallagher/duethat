var base_url = "https://api.projectoxford.ai/luis/v1/application?id=a500a19e-f7ab-4078-9f6c-9b6b8ee3bbeb&subscription-key=598c92029bc24dff8b713c669d774773&q="


var classify = function() {
	var text = document.getElementById("query").value;
	console.log(text);

	var full_url = base_url + text;
	$.getJSON(full_url, function(data) {
		// do something
		showResults(data)
	});
}

var showResults = function(data) {
	var result_box = document.getElementById("result-box");

	var intent = data["intents"][0]["intent"];
	var intent_div = document.createElement("div");
	if (intent == "Schedule") {
		intent_div.innerHTML = "Type: Scheduling.";
	} else if (intent == "To Do") {
		intent_div.innerHTML = "Type: To Do.";
	} else {
		intent_div.innerHTML = "Type: Unknown.";
	}
	result_box.appendChild(intent_div);
	
	var entities = data["entities"];
	for (var i = 0; i < entities.length; i++) {
		var newdiv = document.createElement("div");
		newdiv.id = "entity-"+i;
		newdiv.innerHTML = entities[i]["entity"];
		result_box.appendChild(newdiv);
	}

}

var clear = function() {
	var result_box = document.getElementById("result-box");
	while (result_box.firstChild) {
	    result_box.removeChild(result_box.firstChild);
	}
}