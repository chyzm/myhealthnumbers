function getQueryParams() {
    // Parse URL parameters
    let params = new URLSearchParams(window.location.search);
    return {
        bmi: params.get("bmi"),
        bmiCategory: params.get("bmiCategory"),
        bmr: params.get("bmr"),
        tdee: params.get("tdee"),
        ibw: params.get("ibw"),
        mhr: params.get("mhr")
    };
}

// Retrieve and display results from query parameters
let results = getQueryParams();
document.getElementById("bmi").textContent = results.bmi;
document.getElementById("bmiCategory").textContent = results.bmiCategory;
document.getElementById("bmr").textContent = results.bmr;
document.getElementById("tdee").textContent = results.tdee;
document.getElementById("ibw").textContent = results.ibw;
document.getElementById("mhr").textContent = results.mhr;