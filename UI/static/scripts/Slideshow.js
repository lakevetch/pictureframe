function Slideshow(metadata, imgId, timeoutSec, focus, focusVal) {
    this.metadata = metadata;
    this.length = this.metadata.length;
    this.imgId = imgId;
    this.timeout = timeoutSec * 1000;
    this.focus = focus;
    this.focusVal = focusVal;
    this.index = 0;
    this.intervalID = null;

    this.show_slide = function () {
        let img = document.getElementById(this.imgId);
        img.src = this.metadata[this.index][0];
        console.log(img.src);
    };

    this.play = function () {
        this.show_slide();
        this.intervalID = setInterval(this.next_slide.bind(this), this.timeout);
    };

    this.next_slide = function () {
        this.index += 1;
        if (this.index  === this.length) {
            this.to_root();
        }
        this.focus.value = this.focusVal + this.index;
        this.show_slide();
    };

    this.stop = function () {
        clearInterval(this.intervalID);
    };

    this.skip = function () {
        this.stop();
        this.index += 1;
        if (this.index === this.length) {
            this.to_root(true);
        }
        this.focus.value = this.focusVal + this.index;
        this.play();
        console.log('Skip');
    };

    this.back = function () {
        this.stop();
        this.index -= 1;
        if (this.index < 0) {
            this.to_root(true);
        }
        this.focus.value = this.focusVal + this.index;
        this.play();
        console.log('Back');
    };

    this.to_root = function(skip) {
        this.stop();
        this.focus.value = this.focusVal + this.index;
        let uri = '/?focus=' + this.focus.value;
        if (skip) {
            uri += '&skip';
        }
        window.location = uri;
    };

    this.init = function () {
        this.play();
    };
}