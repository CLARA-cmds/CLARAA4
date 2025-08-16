document.getElementById("predictionForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const loading = document.getElementById("loading");
    const result = document.getElementById("result");

    // Reset styles and show loading
    loading.style.display = "flex";
    result.className = ""; // Clear previous styles
    result.textContent = "";

    const inputs = [
        parseFloat(document.getElementById("input1").value),
        parseFloat(document.getElementById("input2").value),
        parseFloat(document.getElementById("input3").value),
        parseFloat(document.getElementById("input4").value)
    ];

    try {
        // Simulate processing time
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Fetch prediction result
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ inputs })
        });

        const data = await response.json();
        const stage = parseInt(data.stage);

        // Hide loading
        loading.style.display = "none";

        // Apply class based on stage
        let message = "";
        switch (stage) {
            case 0:
                result.classList.add("result-success");
                message = "No sign of liver cancer!";
                window.location.href = "http://127.0.0.1:5000/templates/r0.html";
                return;
            case 1:
                result.classList.add("result-warning");
                message = "Stage 1: Early stage detected. Consider medical consultation.";
                window.location.href = "http://127.0.0.1:5000/templates/r1.html"; //r1
                return;
            case 2:
                result.classList.add("result-danger");
                message = "Stage 2: High risk of liver cancer! Immediate action required!";
                // Redirect to r2.html
                window.location.href = "http://127.0.0.1:5000/templates/r2.html"; //r2
                return; // Stop execution after redirect
            default:
                result.classList.add("result-unknown");
                message = "Unknown stage. Please recheck inputs.";
        }

        result.textContent = message;

        // Store the result in localStorage
        const date = new Date().toLocaleDateString();
        localStorage.setItem("lastScreening", JSON.stringify({
            date: date,
            risk: message,
            stage: stage
        }));
    } catch (error) {
        loading.style.display = "none";
        result.classList.add("result-danger");
        result.textContent = "Error: Unable to predict the stage.";
    }
});
