async function extractVideo() {
    const urlInput = document.getElementById('teraboxUrl').value;
    const player = document.getElementById('mainPlayer');
    const status = document.getElementById('statusMessage');
    const result = document.getElementById('result');
    const downloadBtn = document.getElementById('downloadBtn');

    if (!urlInput) {
        alert("Pehle TeraBox link paste karen!");
        return;
    }

    status.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cloudflare se bypass ho raha hai...';
    status.style.color = "#00ff88";
    result.classList.add('hidden');

    try {
        // Aapka naya Cloudflare Worker URL
        const response = await fetch('https://teraboxpremium.malikmehmoodk821.workers.dev/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: urlInput })
        });

        const data = await response.json();

        if (response.ok && data.status === "success") {
            status.innerHTML = "✅ Video Mil Gayi: " + (data.title || "TeraBox Video");
            
            // Cloudflare Worker se milne wala download link
            player.src = data.download_link;
            downloadBtn.href = data.download_link;
            result.classList.remove('hidden');

            player.play().catch(() => {
                status.innerHTML = "✅ Video par play button dabayen.";
            });
        } 
        else {
            status.style.color = "#ff4757";
            status.innerHTML = "❌ Bypass Fail: TeraBox ne request block kar di hai.";
        }

    } catch (error) {
        console.error("Error:", error);
        status.style.color = "#ff4757";
        status.innerHTML = "❌ Connection Error! Worker check karen.";
    }
}

// WhatsApp Share
function shareWhatsApp() {
    const url = document.getElementById('teraboxUrl').value;
    if (!url) return alert("Kuch share karne ko nahi hai!");
    const text = encodeURIComponent("TeraPlayer Pro par ye video dekhen: " + url);
    window.open(`https://wa.me/?text=${text}`, '_blank');
}

// System Share
async function systemShare() {
    if (navigator.share) {
        try {
            await navigator.share({
                title: 'TeraPlayer Pro',
                text: 'TeraBox Bypass Player!',
                url: window.location.href
            });
        } catch (err) { console.log("Share failed"); }
    } else {
        alert("Aapka browser system share support nahi karta.");
    }
                }
