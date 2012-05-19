$(document).ready(function () {  
	$('#drag_me').draggable({axis : "x" });
	$(document).bind('keydown',function(e){ //set the keydown function as...
		switch(e.which) {
		case 37:    $('#drag_me').animate({
			left:   '+=80'
			    }, 150, function() {
		    });
		    break;
		case 39:    $('#drag_me').animate({
			left:   '-=80'
			    }, 150, function() {
		    });
		    break;
		}

	    });
	//Handle server reloads when user reaches the edge.




	var svgns = "http://www.w3.org/2000/svg";
	var svg_timeline = document.getElementById('svg_timeline');
	for (var i = 0; i < 9000/36; i++) {
	    shape = document.createElementNS(svgns, "line");
	    shape.setAttributeNS(null, "x1", (i*36).toString());
	    shape.setAttributeNS(null, "x2", (i*36).toString());
	    shape.setAttributeNS(null, "y1", "10");
	    shape.setAttributeNS(null, "y2", "30");
	    shape.setAttributeNS(null, "style", "stroke:blue;stroke-width:2")
	    svg_timeline.appendChild(shape);
	    //$('#svg_timeline').append('<line x1="'+ i * 36 + '" y1="10" x2="' + i * 36 + '" y2="30" style="stroke:blue;stroke-width:2"/>');
	}
	
	var options = {
	    lines : {show : true},
	    points : {show : true},
	    xaxis : {tickDecimals : 0, tickSize : 1},
	    grid: {hoverable : true, clickable : true},
	};
	var graph = $('#graph');
	var data = [{
	    "label": "Europe (EU27)",
	    "data": [[1999, 3.0], [2000, 3.9], [2001, 2.0], [2002, 1.2], [2003, 1.3], [2004, 2.5], [2005, 2.0], [2006, 3.1], [2007, 2.9], [2008, 0.9]]
	    },
	    {
		"label": "Japan",
		"data": [[1999, -0.1], [2000, 2.9], [2001, 0.2], [2002, 0.3], [2003, 1.4], [2004, 2.7], [2005, 1.9], [2006, 2.0], [2007, 2.3], [2008, -0.7]]
	    }];
	$.plot(graph, data, options);
	$("#graph").bind("plotclick", function (event, pos, item) {
		if (item) {
		    alert("You clicked point " + item.dataIndex + " in " + item.series.label + ".");
		    plot.highlight(item.series, item.datapoint);
		}
	    });
	//for this, when we call the timeline, we give this timeline a request variable. With this variable we call the server to request a lightbox to show up and populate the lightbox with information or something.

    });


//use tooltip (displays event name when hovering over. and give data). 
//use clickable to be able to click on the individual events that happened and see what happened.

//what is var svgns = "http://www.w3.org/2000/svg"
//Write event handler to load more data when you reach the edge of the page
//Write event handler to move the timeline to the left or right based on arrow keys
//Write event handler to dynamically add data to the page
//http://api.jquery.com/scroll/
//http://stackoverflow.com/questions/3282573/jquery-draggable-and-keyboard-control