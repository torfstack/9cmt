function collectData() {
	var gagid = document.getElementById("input_id").value;
	postData(gagid);
}

function postData(gagid) {
	console.log("Computing with "+gagid);
    $.ajax({
        type: "POST",
        url: "/home/riyil/Code/9cmt/9cmt.py",
        data: { param: gagid },
        success: callbackFunc
    });
}

function callbackFunc(response) {
    console.log("Success");
}