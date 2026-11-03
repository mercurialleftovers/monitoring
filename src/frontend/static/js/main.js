const ws = new WebSocket("/ws");

function EstablishConnection() {
	ws.onmessage = (event) => {
		const sampleData = JSON.parse(event.data);
		// rendering html elements:

		console.log(sampleData);
		// checking existing device div:
		const deviceId = `device_${sampleData.deviceId}`;
		const deviceDiv = document.getElementById(deviceId);
		// const stateImg = document.querySelector(`#${deviceId} .stateCard img`);
		// const stateLabel = document.querySelector(`#${deviceId} .stateCard p`);
		const stateCard = document.querySelector(`#${deviceId} .stateCard`);
		const stateImg = document.querySelector(`#${deviceId} .stateCard img`);

		// switching state related classnames: TOOD(bader)
		console.log(typeof deviceDiv.classList);
		// deviceDiv.classList.remove("inactive");
		// deviceDiv.classList.add("active");

		// stateImg.src = "static/images/active.png";
		// stateLabel.innerText = "active";
		stateCard.classList.remove("inactive");
		stateCard.classList.add("active");
		stateImg.src = "/static/images/icons/flag-green.svg";

		// updating values:
		const temperatureLabel = document.getElementById(`${deviceId}_temperature`);
		const vibrationLabel = document.getElementById(`${deviceId}_vibration`);

		for (const reading of sampleData.sensorReadings) {
			if (reading.sensor === "THERMAL") {
				if (temperatureLabel) {
					temperatureLabel.textContent = reading.value;
				}
			}

			if (reading.sensor === "VIBRATION") {
				if (vibrationLabel) {
					vibrationLabel.textContent = reading.value;
				}
			}
		}
	};

	ws.onclose = (e) => {
		console.log(`closing!`);
		console.log(e);

		EstablishConnection();
	};
}

EstablishConnection();

const delayPromise = (ms) =>
	new Promise((resolve) => {
		setTimeout(() => {
			resolve();
		}, ms);
	});

async function poll() {
	while (homePageEmpty) {
		// debugger;
		await delayPromise(2000);

		fetch("devices/count", { method: "GET" })
			.then((data) => data.json())
			.then((jsoned) => {
				if (jsoned.count > 0) {
					window.location.reload();
					homePageEmpty = false;
				} else {
					console.log(`count: ${jsoned.count}`);
				}
			})
			.catch((err) => {
				alert("error");
				console.error(`error fetching devices count: ${err}`);
			});
	}
}

poll();
