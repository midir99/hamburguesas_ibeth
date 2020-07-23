

const redirectWhenTimeOver = (url) => () => {
    const weekendCounter = document.getElementById('weekend-counter');
    const strDate = weekendCounter.dataset.countdown;
    const then = new Date(strDate);  
    let now = new Date();
    if (now >= then) {    
        window.location.replace(url);
    }
};

setInterval(redirectWhenTimeOver('http://127.0.0.1:5500/menu.html'), 3000);
