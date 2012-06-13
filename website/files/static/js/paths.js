function get_path() {
    return [[1300, 1], [1400, 1], [1184914800, 1], [1192518000, 1], [1197532800, 1], [1212994800, 1], [1214895600, 1], [1272351600, 1], [1291363200, 1]];
    x = {};
    x['word'] = getParameterByName('word');
    post_data = JSON.stringify(x);
    $.ajax({
	    type: 'POST',
		datatype: 'text',
		url: '/load_dynamic',
		data: post_data,
		datatype: 'text',
		complete: function(res, status) {
		if (status == "success") {
		    alert(res.responseText);
		    data = eval('(' + res.responseText + ')')
			return data;
			} else {
		    alert("error");
		    alert(res.responseText);
		}
	    }

	});  
}
function getParameterByName(name)
{
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(window.location.search);
    if(results == null)
	return "";
    else
	return decodeURIComponent(results[1].replace(/\+/g, " "));
}


function scale_array(arr, x, y) {
    var scaled = [];
    for(var i = 0; i < arr.length; i++) {
	scaled.push([arr[i][0] * x, arr[i][1] * y]);
    }
}

function drop_samples(arr, rate) {
    var sampled = [];
    for(var i = 0; i < arr.length; i+=rate) {
	sampled.push(arr[i]);
    }
    return sampled;
}

function average_samples(arr, rate) {
    var sampled = [];
    for(var i = 0; i < rate; i++) {
	sampled.push(arr[i]);
    }

    for(var i = rate; i < arr.length; i++) {
	var total = 0;
	for(var j = 0; j > -rate; j--) {
	    total += arr[i + j][1];
	}
	sampled.push([arr[i][0], total/rate]);
    }
    return sampled;
}

function array_to_path(arr) {
    var path = "M0," + $('#container').height()/2;
    for(var i = 0; i < arr.length; i++) {
	path += "L" + arr[i][0] + "," + ($('#container').height()/2 - arr[i][1]);
    }
    return path;
}
