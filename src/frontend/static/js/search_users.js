const searchBar = document.getElementById("searchBar");
const resetButton = document.getElementById("resetButton");

document.querySelector("#searchSection").classList.remove("hidden");
document.querySelector("#searchSection").classList.add("flex");

function updateDeviceList(kw) {
	const users = document.querySelectorAll(".userCard");

	if (kw === "") {
		for (const user of users) user.classList.remove("hidden");
	}

	const regex = new RegExp(`.*${kw}.*`);

	for (const user of users) {
		let userFullName = user.querySelector(".fullname");
		let userUsername = user.querySelector(".username");

		if (!userFullName || !userUsername) {
			return;
		}

		userFullName = userFullName.textContent;
		userUsername = userUsername.textContent;

		if (regex.test(userFullName) || regex.test(userUsername)) {
			user.classList.remove("hidden");
		} else {
			user.classList.add("hidden");
		}
	}
}

if (searchBar) {
	searchBar.oninput = (e) => {
		const keyword = e.target.value;
		updateDeviceList(keyword);
	};

	resetButton.onclick = (_) => {
		searchBar.value = "";
		updateDeviceList("");
	};
}

function toggleSearchBar() {
	searchBar.value = "";
	updateDeviceList("");
	const searchDiv = document.getElementById("searchDiv");
	searchDiv.classList.toggle("hidden");
}

const searchMagnifier = document.querySelector("#searchMagnifier");
searchMagnifier.onclick = toggleSearchBar;
