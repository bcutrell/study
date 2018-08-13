
// Declare objects that will be used in our state
let target = {
    name: 'Balanced Mix'
}

function randomTicker() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    for (var i = 0; i < 4; i++) text += possible.charAt(Math.floor(Math.random() * possible.length));
        return text;
    }
    function randomPrice() {
    return Math.floor(Math.random() * 1000);
}

function newHolding() {
    return {
        ticker: randomTicker(),
        price: randomPrice()
    }
}
