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
//Basically a repeat of the above function. I'll leave it 
// here for now so that it is easier to merge
function dynamic_draw_path(query, minOffset, maxRange, width, randomColor, paper, layers, togglePath) {
    alert(query + minOffset + maxRange);
    var paths;
    x = {}
    x['word'] = query;
    post_data = JSON.stringify(x);
    $.ajax({
	    type: 'POST',
		async: false,
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
    for(var path_title in paths) {
	var path = paths[path_title];
	paths[path_title] = offset_array(path, minOffset);
    }
    for(var path_title in paths) {
            var path = paths[path_title];
            var scaled = scale_array(path, width/maxRange, 10);
            var averaged = average_samples(scaled, 5);
            var dropped = drop_samples(averaged, 5);
            var pathArr = array_to_path(dropped, true);
	    //pathArr = array_to_path(scaled);
	    //Above is the full data -- which might be good
            var color = randomColor();
            var graph = paper.path(pathArr);
            graph.attr({
              stroke: color,
              fill: color,
              'stroke-width': 3,
              'stroke-opacity': 0.8,
              'fill-opacity': 0.4
	    });

	    layers.path[path_title] = graph;
            layers.status[path_title] = true;
            layers.color[path_title] = color;
	    
            $('#layers_list').append("<li><a class='layer' id='" + path_title + "' href='javascript:;'>" + path_title + "</a></li>");
            $('#' + path_title).css({
              'color': color,
              'font-weight': 'bold'
            });
            $('#' + path_title).click(togglePath(path_title));

    }


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

function offset_array(arr, offset) {
    var shifted = [];
    for(var i = 0; i < arr.length; i++) {
        shifted.push([arr[i][0] - offset, arr[i][1]]);
    }
    return shifted;
}

function scale_array(arr, x, y) {
    var scaled = [];
    for(var i = 0; i < arr.length; i++) {
	scaled.push([arr[i][0] * x, arr[i][1] * y]);
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

function array_to_path(arr, reflect) {
    var path = "M0," + $('#container').height()/2 + "L" + (arr[0][0] - 5 < 0 ? 0 : arr[0][0] - 5) + "," + ($('#container').height()/2);
    for(var i = 0; i < arr.length; i++) {
	path += "L" + arr[i][0] + "," + ($('#container').height()/2 - arr[i][1]);
        if (i < arr.length - 1 && arr[i+1][0] - arr[i][0] > 10)
          path += "L" + (arr[i][0] + 5) + "," + ($('#container').height()/2) + "L" + (arr[i+1][0] - 5) + "," + ($('#container').height()/2);
    }
    path += "L" + $('#container').width() + "," + $('#container').height()/2 + "L0," + $('#container').height()/2;

    if (reflect) {
      path += "M0," + $('#container').height()/2 + "L" + (arr[0][0] - 5 < 0 ? 0 : arr[0][0] - 5) + "," + ($('#container').height()/2);
      for(var i = 0; i < arr.length; i++) {
          path += "L" + arr[i][0] + "," + ($('#container').height()/2 + arr[i][1]);
          if (i < arr.length - 1 && arr[i+1][0] - arr[i][0] > 10)
            path += "L" + (arr[i][0] + 5) + "," + ($('#container').height()/2) + "L" + (arr[i+1][0] - 5) + "," + ($('#container').height()/2);
      }
      path += "L" + $('#container').width() + "," + $('#container').height()/2 + "L0," + $('#container').height()/2;
    }

    return path;
}
