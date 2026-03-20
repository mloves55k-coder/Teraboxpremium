async function extractVideo() {
    const urlInput = document.getElementById('teraboxUrl').value;
    const player = document.getElementById('mainPlayer');
    const status = document.getElementById('statusMessage');
    const result = document.getElementById('result');

    if (!urlInput) return alert("Please paste a link!");

    status.innerHTML = "🚀 Bypassing via Vercel Server...";
    status.style.color = "#00ff88";

    try {
        // CHANGE THIS URL after deploying to Vercel
        const response = await fetch('/api/extract', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: urlInput })
        });

        const data = await response.json();

        if (response.ok && data.status === "success") {
            status.innerHTML = "✅ Found: " + data.title;
            player.src = data.download_link;
            document.getElementById('downloadBtn').href = data.download_link;
            result.classList.remove('hidden');
            player.play();
        } else if (response.status === 403) {
            status.innerHTML = `<button onclick="window.open('${data.verify_url}', '_blank')" style="background:orange; padding:10px; border-radius:5px;">Solve Captcha on TeraBox</button>`;
        } else {
            status.innerHTML = "❌ Bypass Failed: " + (data.message || "Unknown error");
        }
    } catch (e) {
        status.innerHTML = "❌ Connection Error!";
    }
}
