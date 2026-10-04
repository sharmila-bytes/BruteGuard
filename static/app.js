const countdown = document.getElementById("countdown");

if (countdown) {
    let seconds = Number(countdown.dataset.seconds || 0);

    const tick = () => {
        countdown.textContent = `${seconds}s`;
        if (seconds <= 0) {
            window.location.reload();
            return;
        }
        seconds -= 1;
        window.setTimeout(tick, 1000);
    };

    tick();
}
