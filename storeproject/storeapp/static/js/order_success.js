// 🎉 CONFETTI
const canvas = document.getElementById("confetti");

if (canvas) {
    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    let pieces = [];

    for (let i = 0; i < 200; i++) {
        pieces.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 6 + 2,
            speed: Math.random() * 3 + 2
        });
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        pieces.forEach(p => {
            ctx.fillStyle = `hsl(${Math.random()*360},100%,50%)`;
            ctx.fillRect(p.x, p.y, p.size, p.size);
        });

        update();
    }

    function update() {
        pieces.forEach(p => {
            p.y += p.speed;

            if (p.y > canvas.height) {
                p.y = 0;
                p.x = Math.random() * canvas.width;
            }
        });
    }

    setInterval(draw, 30);
}


// ⏳ AUTO REDIRECT
let timeLeft = 5;
const countdown = document.getElementById("countdown");

if (countdown) {
    const timer = setInterval(() => {
        timeLeft--;

        countdown.innerText = timeLeft;

        if (timeLeft <= 0) {
            clearInterval(timer);
            window.location.href = "/";
        }

    }, 1000);
}