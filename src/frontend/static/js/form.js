const fileUpload = document.querySelector("input[type=file]");
const registerButton = document.querySelector(".selectFileButton");

// clicking the "choose an image" button activates the file input
registerButton.onclick = (_) => {
	fileUpload.click();
};

// setting the uploaded image as the background-image of the image input field
fileUpload.onchange = (e) => {
	fileURL = URL.createObjectURL(e.target.files[0]);
	fileUpload.style["background-image"] = `url(${fileURL})`;
};
