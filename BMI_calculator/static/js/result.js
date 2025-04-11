function submitBMI() {
  // Get input values
  const age = document.getElementById('age').value;
  const weight = document.getElementById('weight').value;
  const height = document.getElementById('height').value;
  const comments = document.getElementById('comments').value;

  // Validate inputs
  if (!age || !weight || !height) {
    alert('Please fill out all required fields.');
    return;
  }

  // Calculate BMI
  const bmi = (weight / (height * height)).toFixed(2);
  let status;

  // Determine BMI status
  if (bmi < 18.5) {
    status = 'Underweight';
  } else if (bmi < 24.9) {
    status = 'Normal weight';
  } else if (bmi < 29.9) {
    status = 'Overweight';
  } else {
    status = 'Obese';
  }

  // Construct query string
  const queryString = `age=${encodeURIComponent(age)}&bmi=${encodeURIComponent(bmi)}&status=${encodeURIComponent(status)}&comments=${encodeURIComponent(comments)}`;

  // Redirect to result view
  window.location.href = `/result/?${queryString}`;
}
