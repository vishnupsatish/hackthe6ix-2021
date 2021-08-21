const updateButton = $("#update-button");

const updateClick = (id) => {
	const description = $("#description").text();
	const code = $("#code").text();
	const triggerPhrase = $("#trigger_phrase").text();
	request = $.ajax("/commands", {
		type: "PATCH",
		data: {
			"id": id,
			"trigger_phrase": triggerPhrase,
			"description": description,
			"code": code,
		},
	});
	
	request.done((response, textStatus, errorThrown) => {
		console.log(response);
	})
};

const changeModalDisplay = () => {
	const addButton = $("#command-panel");
	const display = addButton.css("display");
	
	if (display === "none") {
		addButton.css("display", "flex");
		addButton.css("flex-direction", "column");
	} else {
		addButton.css("display", "none");
	}
}