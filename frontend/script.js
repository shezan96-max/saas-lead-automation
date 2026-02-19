document.getElementById("leadForm").addEventListener("submit",async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    await fetch("/submit-lead?client_name=demo", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(data)
    });

    alert("Lead Submitted!");
    this.reset();
})