async function sendMessage() {
    let message =
        document.getElementById("message").value;
    let response = await fetch(
        "/chat",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        }
    );
    let data = await response.json();
    document.getElementById("chat").innerHTML +=
        `<p><b>You:</b> ${message}</p>`;
    document.getElementById("chat").innerHTML +=
        `<p><b>Bot:</b> ${JSON.stringify(data.response, null, 2)}</p>`;
}