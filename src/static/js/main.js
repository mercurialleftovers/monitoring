const ws = new WebSocket("/ws");

function EstablishConnection() {
	// debugger;
	ws.onmessage = function(event) {
		// console.log(`received:\n${event.sampleData}`);
		const sampleData = JSON.parse(event.data);
		// rendering html elements:

		console.log(sampleData);
		// checking existing device div:
		let deviceId = `device_${sampleData.deviceId}`
		let deviceDiv = document.getElementById(deviceId);

		// creating the container div, and subsequent child divs
		if (!deviceDiv) { // one time setup per device
			deviceDiv = document.createElement("div");
			deviceDiv.id = deviceId;
			deviceDiv.classList.add("device");
			// adding the device identifier header
			let deviceLabelHeader = document.createElement("h2");
			let deviceLabelText = document.createTextNode(sampleData["name"]);
			deviceLabelHeader.appendChild(deviceLabelText);
			deviceLabelHeader.classList.add("deviceName")
			// temperature
			let temperatureHeader = document.createElement("h3");
			let temperatureLabel = document.createElement("p");
			let temperatureHeaderText = document.createTextNode(`temperature`);
			temperatureLabel.id = `${deviceId}_temperature`
			temperatureHeader.appendChild(temperatureHeaderText)
			// vibration
			let vibrationHeader = document.createElement("h3");
			let vibrationLabel = document.createElement("p");
			let vibrationHeaderText = document.createTextNode(`vibration`);
			vibrationLabel.id = `${deviceId}_vibration`
			vibrationHeader.appendChild(vibrationHeaderText)
			// adding elements
			deviceDiv.appendChild(deviceLabelHeader);
			deviceDiv.appendChild(temperatureHeader);
			deviceDiv.appendChild(temperatureLabel);
			deviceDiv.appendChild(vibrationHeader);
			deviceDiv.appendChild(vibrationLabel);

			// inserting device information into deviceDiv and rendering the latter:

			fetch("/device/byid?id=" + sampleData["deviceId"], { method: "POST" }).then(data => data.json()).then(deviceData => {
				console.log(deviceData);
				// rendering device name
				deviceLabelText.data = deviceData["deviceName"];
				// rending department
				// departmentLabel.data = deviceData["departement"];
				const AGITATOR_IMG = document.createElement("img");
				const MOTOR_IMG = document.createElement("img");

				AGITATOR_IMG.src = "/static/device_types/agitator.png";
				MOTOR_IMG.src = "/static/device_types/motor.png";

				switch (deviceData["category"]) {
					case "AGITATOR":
						deviceDiv.appendChild(AGITATOR_IMG);
						document.getElementsByClassName("category agitators")[0].appendChild(deviceDiv);
						break;
					case "MOTOR":
						deviceDiv.appendChild(MOTOR_IMG);
						document.getElementsByClassName("category motors")[0].appendChild(deviceDiv);
						break;
				}
			}).catch(err => {
				console.log(`cannot render device: ${err}`)
			});
		}

		// updating values:
		let temperatureLabel = document.getElementById(`${deviceId}_temperature`);
		let vibrationLabel = document.getElementById(`${deviceId}_vibration`);

		for (let reading of sampleData.sensorReadings) {
			if (reading["sensor"] == "THERMAL") {
				if (temperatureLabel) {
					temperatureLabel.textContent = reading["value"];
				}
			}

			if (reading["sensor"] == "VIBRATION") {
				if (vibrationLabel) {
					vibrationLabel.textContent = reading["value"];
				}
			}
		}
	}

	ws.onclose = EstablishConnection;
}

EstablishConnection();
