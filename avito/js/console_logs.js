console.logs = [];
XMLHttpRequest.prototype.realSend = XMLHttpRequest.prototype.send;
XMLHttpRequest.prototype.send = function(value) {
    this.addEventListener("progress", function(){
        console.logs.push(this.responseURL);
    }, false);
    this.realSend(value);
};