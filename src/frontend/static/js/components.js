let deviceViewTemplate = document.createElement("template");
deviceViewTemplate.innerHTML = `
	<div class="device">
		<div class="idCard">
			<img class="deviceImg" src="" alt="device image here"/>
			<p class="deviceName"><device name here></p>
		</div>

		<div class="departmentCard">
			<p class="deviceDepartment"><device department here></p>
			<img src="#" alt="device department logo"/>
		</div>

		<p class="deviceCategory"><device category here></p>

		<div class="monitor">
			<p class="temperatureValue"><temperature value herer<</p>
			<p class="vibrationValue"><vibration value herer<</p>
		</div>
	</div>
`

class DeviceView extends HTMLElement {
	constructor() {
		super();
		this.innerHTML = "My Custom HTML Element";
	}
}

customElements.define("custom-element", DeviceView);
