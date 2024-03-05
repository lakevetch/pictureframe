function Root() {
    this.head = document.getElementsByName('head').item(0);
    this.body = document.getElementsByName('body').item(0);
    this.metadata = document.getElementById('metadata');
    this.timeoutSec = document.getElementById('timeout-sec');
    this.focus = document.getElementById('focus');
    this.focusForm = document.getElementById('focus-form');
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
        let focusId = this.focus.id;
        return new Slideshow(metadata, 'slide', timeoutSec, focusId);
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
            window.addEventListener('dblclick', () => {
                if (elem.style.display === 'flex') {
                    elem.style.display = 'none';
                } else {
                    elem.style.display = 'flex';
                    elem.classList.remove('clicked');
                }
            });
        }
    };

    this.setupControls = function () {
        let slideshow = this.slideshow;
        let skip = this.skip;
        let back = this.back;
        let settings = this.settings;
        skip.addEventListener('click', () => {
            skip.classList.add('clicked');
            back.classList.remove('clicked');
            settings.classList.remove('clicked');
            slideshow.skip.bind(slideshow).call();
        });
        back.addEventListener('click', () => {
            skip.classList.remove('clicked');
            back.classList.add('clicked');
            settings.classList.remove('clicked');
            slideshow.back.bind(slideshow).call();
        });
        settings.addEventListener('click', () => {
            skip.classList.remove('clicked');
            back.classList.remove('clicked');
            settings.classList.add('clicked');
            this.focusForm.submit();
        });
    }
}

window.addEventListener('load', () => {
    console.log('hello world');
    let root = new Root();
    console.log(root);
    root.init();
    console.log('init complete');
});