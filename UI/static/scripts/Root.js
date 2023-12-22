function Root() {
    this.head = document.getElementsByName('head').item(0);
    this.body = document.getElementsByName('body').item(0);
    this.metadata = document.getElementById('metadata');
    this.timeoutSec = document.getElementById('timeout-sec');
    this.img = document.getElementById('slide');
    this.controls = document.getElementsByClassName('control-panel');
    this.back = document.getElementById('back');
    this.skip = document.getElementById('skip');
    this.settings = document.getElementById('settings');
    this.slideshow = null;

    this.init = function () {
        this.slideshow = this.setupSlideshow();
        this.startSlideshow();
        let timeout = setTimeout(this.dailyReset.bind(this), 86400000);
        this.showControls();
        this.setupControls();
    };

    this.setupSlideshow = function () {
        let metadata = JSON.parse(this.metadata.value);
        let timeoutSec = this.timeoutSec.value;
        return new Slideshow(metadata, 'slide', timeoutSec);
    };

    this.startSlideshow = function () {
        this.slideshow.init();
    };

    this.dailyReset = function () {
        window.location = '/';
    };

    this.showControls = function () {
        for (let i = 0; i < this.controls.length; i++) {
            let elem = this.controls.item(i);
            window.addEventListener('click', () => {
                elem.classList.remove('clicked');
                if (elem.style.display === 'none') {
                    elem.style.display ='flex';
                    let timeout = setTimeout(() => {
                        elem.style.display = 'none';
                    }, 4000);
                } else {
                    elem.style.display = 'none';
                }
            });
        }
    };

    this.setupControls = function () {
        let slideshow = this.slideshow;
        this.skip.addEventListener('click', slideshow.skip.bind(slideshow));
        this.back.addEventListener('click', slideshow.back.bind(slideshow));
        this.settings.addEventListener('click', () => {
            window.location = '/settings';
        });
    }
}

window.addEventListener('load', () => {
    console.log('hello world');
    let root = new Root();
    root.init();
    console.log('init complete');
});