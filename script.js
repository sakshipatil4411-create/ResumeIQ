
const form = document.getElementById("resumeForm");
const message = document.getElementById("message");

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const resume = document.getElementById("resume").files[0];
    const jobDescription = document.getElementById("jobDescription").value.trim();

    if (!resume) {
        message.innerHTML = "❌ Please upload your resume.";
        return;
    }

    if (!jobDescription) {
        message.innerHTML = "❌ Please enter the job description.";
        return;
    }

    message.innerHTML = "⏳ Analyzing your resume...";

    // Temporary frontend demo
    setTimeout(function () {
        message.innerHTML =
            "✅ Resume uploaded successfully! AI analysis will be processed by the Python backend.";
    }, 1500);
});
