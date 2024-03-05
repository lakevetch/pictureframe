function Slideshow(metadata, imgId, timeoutSec, focusId) {
    this.metadata = metadata;
    this.length = this.metadata.length;
    this.imgId = imgId;
    this.timeout = timeoutSec * 1000;
    this.focusId = focusId;
    this.index = 0;
    this.intervalID = null;

    this.show_slide = function () {
        let img = document.getElementById(this.imgId);
        img.src = this.metadata[this.index][0];
        let focus = document.getElementById(this.focusId);
        focus.value = this.index;
        console.log(img.src);
    };

    this.play = function () {
        this.show_slide();
        this.intervalID = setInterval(this.next_slide.bind(this), this.timeout);
    };

    this.next_slide = function () {
        this.index += 1;
        if (this.index  === this.length) {
            this.index = 0;
        }
        this.show_slide();
    };

    this.stop = function () {
        clearInterval(this.intervalID);
    };

    this.skip = function () {
        this.stop();
        this.index += 1;
        if (this.index === this.length) {
            this.index = 0;
        }
        this.play();
        console.log('Skip');
    }

    this.back = function () {
        this.stop();
        this.index -= 1;
        if (this.index < 0) {
            this.index = this.index + this.length;
        }
        this.play();
        console.log('Back');
    }

    this.init = function () {
        // let focus = document.getElementById(this.focusId);
        // this.index = parseInt(focus.value);
        console.log(this);
        this.play();
    };
}