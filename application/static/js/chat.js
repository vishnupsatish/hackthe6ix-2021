const plusButton = document.getElementById("add-chat");

plusButton.addEventListener("click", () => {
	const prompt = window.prompt('Enter the username of the friend you want to add!');
	console.log(prompt);
});

$("#add-chat").on("click", () => {
	console.log("Clicked.");
	const friend = window.prompt("Enter the username of a friend!");

	alert("Friend added.");
});