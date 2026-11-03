class Plot {
	// make a function plotter
	constructor() {
		this.ctx = plottingCanvas.getContext("2d");
		this.width = plottingCanvas.getAttribute("width");
		this.height = plottingCanvas.getAttribute("height");

		console.log(this.ctx);
		console.log(this.width);
		console.log(this.height);
	}

	plot(x, y) {}

	// make a coordinate mapper

	map_coord(x, y) {}
}

new Plot();
