$(document).ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?                                                                                        
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute                                                                                                
            var host = document.location.host; // host + port                                                                                                      
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin                                                                                               
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.                                                                           
                !(/^(\/\/|http:|https:).*/.test(url));
        }

        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });

function get_paths() {
    var paths;
    x = {};
    x['word'] = getParameterByName('word');
    post_data = JSON.stringify(x);
    $.ajax({
	    type: 'POST',
                async: false,
		datatype: 'text',
		url: '/load_dynamic',
		data: post_data,
		complete: function(res, status) {
		if (status == "success") {
		    paths = eval('(' + res.responseText + ')');
		} else {
		    alert("error");
		    alert(res.responseText);
		}
	    }

	});
    return paths;
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
	scaled.push([(arr[i][0] - arr[0][0]) / x, arr[i][1] * y]);
    }
    return scaled;
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
