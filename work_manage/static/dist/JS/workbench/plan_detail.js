let ifr = document.getElementById("ifr");
let content = document.getElementById("editor-content").innerHTML;
content =
    '<html>'
    + '  <head>'
    + '    <link href="/static/dist/CSS/ckeditor_style.css" rel="stylesheet" >\n'
    + '  </head>'
    + '  <body class="' + ifr.dataset.bodyClass + '">'
    + content
    + '  </body>'
    + '</html>';
ifr.srcdoc = content

function setIframeHeight(iframe) {
    return function _callback() {
        if (iframe) {
            let iframeWin = iframe.contentWindow || iframe.contentDocument.parentWindow;
            if (iframeWin.document.body) {
                let height = 10 + (iframeWin.document.documentElement.scrollHeight || iframeWin.document.body.scrollHeight);
                iframe.height = height > 550 ? 550 : height;
            }
        }
    }
}

var IframeOnClick = {
    resolution: 200,
    iframes: [],
    interval: null,
    Iframe: function () {
        this.element = arguments[0];
        this.cb = arguments[1];
        this.hasTracked = false;
    },
    track: function (element, cb) {
        this.iframes.push(new this.Iframe(element, cb));
        if (!this.interval) {
            var _this = this;
            this.interval = setInterval(function () {
                _this.checkClick();
            }, this.resolution);
        }
    },
    checkClick: function () {
        if (document.activeElement) {
            var activeElement = document.activeElement;
            for (var i in this.iframes) {
                if (activeElement === this.iframes[i].element) { // user is in this Iframe
                    if (this.iframes[i].hasTracked == false) {
                        this.iframes[i].cb.apply(window, []);
                        this.iframes[i].hasTracked = true;
                    }
                } else {
                    this.iframes[i].hasTracked = false;
                }
            }
        }
    }
};

IframeOnClick.track(ifr, setIframeHeight(ifr) );