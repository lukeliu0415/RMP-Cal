'use strict';

/*
 * RateMyProfessor Chrome Extension
 * Not for public distribution
 * Dev: Luke Liu
 * Version: Development
 */

checkDivs();

/*
 * Checks the professor names and cleans them so they can be checked with
 * RateMyProfessor.com
 */
async function checkDivs() {
	console.log('checking...');
	let div = document.querySelector("div.detail-instructors");
	let count = 0;
	while (div == null && count < 20) {
		await sleep(200);
		div = document.querySelector("div.detail-instructors");
		count++;
	}
	if (div == null) {
		console.log('No professors found');
		return;
	}

	let professor_elements = div.querySelectorAll("span");

	// for (let i = 1; i < professor_elements.length; i++) {
	// 	let professor_element = professor_elements[i];
	// 	let professor_name = professor_element.innerHTML;
	// 	professor_element.innerHTML = professor_name + " (Rating: Loading)";
	// }
	
	let url = 'https://rmpcal-backend.herokuapp.com/ratings/?url=' + window.location.href;
	// let url = 'http://127.0.0.1:8000/ratings/?url=' + window.location.href;
	fetch(url).then(function (response) {
		return response.json();
	}).then((json) => {
		for (let i = 1; i < professor_elements.length; i++) {
			let professor_element = professor_elements[i];
			let professor_name = professor_element.innerHTML;
			if (json[i-1] === -1) {
				professor_element.innerHTML = professor_name + " (Rating: unavailable)";
			} else {
				professor_element.innerHTML = professor_name + " (Rating: " + json[i-1] + ")";
			}
		}
	}).catch((err) => {
		console.log(err);
	});

	url = 'https://rmpcal-backend.herokuapp.com/grades/?url=' + window.location.href;
	// url = 'http://127.0.0.1:8000/grades/?url=' + window.location.href;
	fetch(url).then(function (response) {
		return response.json();
	}).then((json) => {
		let div = document.querySelector("div.detail-class-units");
		let tag = document.createElement("p");
		tag.innerHTML = "Average GPA: " + json;
		div.appendChild(tag);
	}).catch((err) => {
		console.log(err);
	});

	// if (div != null) {
	// 	divs.forEach(function (el) {
	// 		let instructorName = el.children[0];
	// 		if (instructorName != null) {
	// 			let insideText = instructorName.innerText;
	// 			if (insideText.toLowerCase().includes("view syllabus")) {
	// 				instructorName.innerText = insideText.substr(0, insideText.indexOf("View syllabus"));
	// 				insideText = instructorName.innerText;
	// 			}
	// 			if (!insideText.includes("--")) {
	// 				let splitIt = (insideText).split(" ");
	// 				if (splitIt[1].includes(".") || splitIt[1].length == 1 | splitIt[2] != null) {
	// 					let cleanName = splitIt[0] + " " + splitIt[2];
	// 					instructorName.innerText = cleanName;
	// 				}
	// 				instructorNames.push(instructorName);

	// 			}
	// 		}
	// 	});
	// 	for (let i = 0; i < instructorNames.length; i++) {
	// 		getScores(instructorNames[i].innerText, instructorNames[i]);
	// 	}
	// } else {
	// 	console.log("Unable to find professors on this page.");
	// }
}

/*
 * Sleep function used to allow for the browser to load the course information
 */
function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}

/*
 * Loads creates the HTML elements that will be inserted into the page based
 * on the returned content
 */
function createElements(message, originalEl) {
	if (message.status == "success") {
		let quality = message.overallQuality;
		let takeAgain = message.takeAgain;
		let difficulty = message.difficulty;
		let link = message.url;
		let qualityEl = $(`<p>Overall Quality: ${quality}</p>`);
		let takeAgainEl = $(`<p>Would Take Again: ${takeAgain}</p>`);
		let difficultyEl = $(`<p>Level of Difficulty: ${difficulty}</p>`);
		let linkEl = $(`<a href=${link} target='_blank'>Link</a>`);
		let overallDiv = $("<div></div>");
		$(originalEl).css('text-align', 'center');
		let upperEl = $(originalEl).parents('.course-section-instructor');
		overallDiv.append(qualityEl, takeAgainEl, difficultyEl, linkEl);
		overallDiv.addClass("rmp-info");
		$(originalEl).children('.rmp-loading').remove();
		upperEl.append(overallDiv);
	} else {
		$(originalEl).children('.rmp-loading').remove();
		let failedDiv = $('<p>No RMP data!</p>');
		let upperEl = $(originalEl).parents('.course-section-instructor');
		upperEl.append(failedDiv);
	}
}

/*
 * Sends the professor names to be checked and returns a response with content
 * that will be injected into the page
 */
function getScores(name, element) {
	$(element).append($("<p class='rmp-loading'>Loading!</p>"));
	let cleanedName = name.replace(" ", "+");
	// let url = `https://students.washington.edu/joncady/projects/ratemyprofessor/rmp.php?name=${cleanedName}`;
	var el = element;
	// fetch(url).then(function (reponse) {
	// 	return reponse.json();
	// }).then(function (myJson) {
	// 	createElements(myJson, el);
	// });
	createElements({
		"status": "success",
		"overallQuality": "10",
		"takeAgain": "10",
		"difficulty": "8",
		"url": "http:\/\/www.ratemyprofessors.com\/ShowRatings.jsp?tid=1728938&showMyProfs=true"
	}, el)
}
