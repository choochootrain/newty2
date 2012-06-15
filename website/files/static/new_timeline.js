$(document).ready(function() {
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
			    } else {
			alert("error");
		    }
		}

	    });

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


    }