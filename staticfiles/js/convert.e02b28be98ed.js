function convertFeetToMeters() {
    const feetInput = document.getElementById('feet').value;
    const feet = parseFloat(feetInput);
    const resultElement = document.getElementById('conversionResult');

    if (!isNaN(feet)) {
        const meters = (feet * 30.48).toFixed(2);
        resultElement.textContent = `${feet} feet is approximately ${meters} centimeter.`;
    } else {
        resultElement.textContent = feetInput.trim() === "" 
            ? ""  // Clear the message if input is empty
            : "Please enter a valid number.";
    }
}