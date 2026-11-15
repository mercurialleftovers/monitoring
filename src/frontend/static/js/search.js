const searchBar = document.getElementById("searchBar");
const resetButton = document.getElementById("resetButton");

function updateDeviceList(kw) {
	const devices = document.querySelectorAll(".deviceContainer");

	if (kw === "") {
		for (const device of devices) device.classList.remove("hidden");
	}

	const regex = new RegExp(`.*${kw}.*`);

	for (const device of devices) {
		let deviceName = device.querySelector(".deviceName");
		let deviceTag = device.querySelector(".deviceTag");

		if (!deviceName || !deviceTag) {
			return;
		}

		deviceName = deviceName.textContent;
		deviceTag = deviceTag.textContent;

		if (regex.test(deviceName) || regex.test(deviceTag)) {
			device.classList.remove("hidden");
		} else {
			device.classList.add("hidden");
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
	const searchDiv = document.getElementById("searchDiv");

	console.log(searchDiv);

	if (searchDiv.classList.contains("hidden")) {
		searchDiv.classList.remove("hidden");
	} else {
		searchDiv.classList.add("hidden");
	}
}
