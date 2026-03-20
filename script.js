async function extractVideo() {
    const urlInput = document.getElementById('teraboxUrl').value;
    const player = document.getElementById('mainPlayer');
    const status = document.getElementById('statusMessage');
    const result = document.getElementById('result');

    if (!urlInput) return alert("Please paste a link!");

    status.innerHTML = "🚀 Fetching from Vercel Server...";
    status.style.color = "#00ff88";

    try {
        // Yahan aapne apna Vercel link use karna hai
        const response = await fetch('https://ium.vercel.app/api/extract', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: urlInput })
        });

        const data = await response.json();

        if (response.ok && data.status === "success") {
            status.innerHTML = "✅ Title: " + data.title;
            player.src = data.download_link;
            document.getElementById('downloadBtn').href = data.download_link;
            result.classList.remove('hidden');
            player.play();
        } else {
            // Agar block ya captcha aaye toh message dikhayein
            status.innerHTML = "❌ Bypass failed: " + (data.message || "Try again later");
            status.style.color = "#ff4d4d";
        }
    } catch (e) {
        status.innerHTML = "❌ Connection Error!";
        status.style.color = "#ff4d4d";
    }
                      }
