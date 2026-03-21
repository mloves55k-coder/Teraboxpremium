// 1. Video.js Player ko initialize karen (ye top par hona chahiye)
var player = videojs('mainPlayer', {
    fluid: true, // Player ko responsive banata hai
    playbackRates: [0.5, 1, 1.5, 2],
    controlBar: {
        skipButtons: {
            forward: 10,
            backward: 10
        }
    }
});

async function extractVideo() {
    const urlInput = document.getElementById('teraboxUrl').value.trim();
    const status = document.getElementById('statusMessage');
    const result = document.getElementById('result');
    const downloadBtn = document.getElementById('downloadBtn');

    if (!urlInput) {
        alert("Pehle TeraBox link paste karen!");
        return;
    }

    // UI Reset
    status.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cloudflare se bypass ho raha hai...';
    status.style.color = "#00ff88";
    result.classList.add('hidden');

    try {
        // Aapka Cloudflare Worker URL
        const workerApi = 'https://teraboxpremium.malikmehmoodk821.workers.dev/';

        const response = await fetch(workerApi, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: urlInput })
        });

        const data = await response.json();

        if (response.ok && data.status === "success") {
            const videoTitle = data.title || "TeraBox Video";
            status.innerHTML = "✅ Video Mil Gayi: " + videoTitle;
            
            // 2. Video.js mein source set karne ka naya tareeqa
            player.src({
                src: data.download_link,
                type: 'video/mp4'
            });

            // Download button par direct link (ya proxy link) set karna
            downloadBtn.href = data.download_link;
            result.classList.remove('hidden');

            // Video automatically play karne ki koshish
            player.ready(function() {
                player.play().catch(() => {
                    status.innerHTML = "✅ Video par play button dabayen.";
                });
            });

        } else {
            status.style.color = "#ff4757";
            status.innerHTML = "❌ Bypass Fail: TeraBox ne request block kar di hai.";
        }

    } catch (error) {
        console.error("Error:", error);
        status.style.color = "#ff4757";
        status.innerHTML = "❌ Connection Error! Worker ya Internet check karen.";
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
