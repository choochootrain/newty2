/*My JS */
jQuery(document).ready(function ($) {
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

	$('#signup').click(function() {
		var toSubmit = {};
		//toSubmit['username'] = $('#username_signup').val()
		toSubmit['email'] = $('#email_signup').val()
		    toSubmit['password'] = $('#password_signup').val()
		    toSubmit['first'] = $('#first_signup').val()
		    toSubmit['last'] = $('#last_signup').val()
		    var data = JSON.stringify(toSubmit);
		$('#signup_dialog').dialog('close');
		$.ajax({
			type: 'POST',
			    dataType: 'text',
			    url: '/createUser/',
			    data: data,
			    dataType: 'text',
			    success: function(g) {
			    $('#username_signup').val('');
			    $('#email_signup').val('');
			    $('#password_signup').val('');
			    $('#first_signup').val('');
			    $('#last_signup').val('');
			    alertbox("success", g);

			}
		    });
	    });

	$('#signup_cancel').click(function() {
		$('#signup_dialog').dialog('close');
		$("#signup_form").slideToggle('slow', function () {
			//done fading
		    });
		$("#create_profile_container").slideToggle('slow', function () {
			//done fading
		    });
		$("#create_profile_tutor_container").slideToggle('slow', function () {
			//done fading
		    });
	    });

	$('#signup_tutor_cancel').click(function() {
		$("#signup_form_tutor").slideToggle('slow', function () {
			//done fading
		    });
		$("#create_profile_container").slideToggle('slow', function () {
			//done fading
		    });
		$("#create_profile_tutor_container").slideToggle('slow', function () {
			//done fading
		    });
	    });


	$('#login').click(function() {
		var toSubmit = {};
		toSubmit['email'] = $('#username_login').val()
		    toSubmit['password'] = $('#password_login').val()
		    var data = JSON.stringify(toSubmit);
		$.ajax({
			type: 'POST',
			    dataType: 'text',
			    url: '/login/',
			    data: data,
			    dataType: 'text',
			    success: function(g) {
			    if(g !== 'wrong password') {
				$("#login_form").slideToggle('slow', function () {
					$("#username_login").val('');
					$("#password_login").val('');
				    });
				$("#logout_form").slideToggle('slow', function () {
					//done fading                                                                                                                                                                     
				    });
				$('#welcome_name').html("<h3 class='white'>Welcome, " + g + "</h3>");
			    } else {
				alertbox("error", "Your email and password do not match. Please try again.");
			    }
			}
		    });

	    });



	    $('#logout').click(function() {
		    $.ajax({
			    type: 'POST',
				dataType: 'text',
				url: '/logout/',
				data: '',
				dataType: 'text',
				success: function(g) {
				$("#login_form").slideToggle('slow', function () {
					//done fading                                                                                                                                                                         
				    });
				$("#logout_form").slideToggle('slow', function () {
					//done fading                                                                                                                                                                         
				    });
			    }
			});
		});

            
});
