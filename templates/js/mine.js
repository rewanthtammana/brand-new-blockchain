var mine;
let result = document.getElementById('result-list');

var Client = (function() {
    // Constructor
    function Client(id) {
        this.id = id;
    };

    // add the methods to the prototype so that all of the 
    // start method initiates the mining process and adds the
    // new block to the blockchain
    Client.prototype.start = function() {
        const id = this.id;
        let data = {
            "data": `Block added by node ${id}`,
            "id": id
        };
        console.log(data);
        let params = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(data)
        };
        $.ajax({
            url: URL,
            type: 'POST',
            data: data,
            dataType: 'json',
            success: function (response) {
                console.log(response);
                result.innerHTML = result.innerHTML + `<tr><td>${response["msg"]}</td><td>${response["timestamp"]}</td><td>${response["hash"]}</td></tr>`;
            },
            error: function (err) {
                console.log('error', arguments);
                console.log(err);
            }
        });
    };

    return Client;
})();