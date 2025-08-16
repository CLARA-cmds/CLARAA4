window.onload = function() {
    const lastScreening = JSON.parse(localStorage.getItem("lastScreening"));
    if (lastScreening) {
        const historyContainer = document.getElementById("historyContainer");

        // Create a new history box for the last screening result
        const historyBox = document.createElement("div");
        historyBox.classList.add("hbox");

        const dateElement = document.createElement("div");
        dateElement.classList.add("upp");
        dateElement.innerHTML = `<h2>${lastScreening.date}</h2>`;

        const riskElement = document.createElement("div");
        riskElement.classList.add("ht");
        riskElement.innerHTML = `<h2>${lastScreening.risk}</h2>`;

        const downloadButton = document.createElement("button");
        downloadButton.classList.add("downloadBtn");
        downloadButton.innerHTML = `<h1><i class='bx bxs-download'></i></h1><h2>Export PDF</h2>`;

        // Add event listener to the download button to trigger PDF export
        downloadButton.addEventListener("click", function() {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            doc.text("Date: " + lastScreening.date, 10, 10);
            doc.text("Risk: " + lastScreening.risk, 10, 20);
            doc.text("Stage: " + lastScreening.stage, 10, 30);
            doc.save("history_report_" + lastScreening.date.replace(/ /g, "_") + ".pdf");
        });

        // Append all the elements to the history box
        historyBox.appendChild(dateElement);
        historyBox.appendChild(riskElement);
        historyBox.appendChild(downloadButton);

        // Append the history box to the container
        historyContainer.appendChild(historyBox);
    } else {
        // Display a message if no screening data is available in localStorage
        const historyContainer = document.getElementById("historyContainer");
        historyContainer.innerHTML = "<p>No screening data available.</p>";
    }
}
