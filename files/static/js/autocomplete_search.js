$(document).ready(function () {  
  $(function() {
	  var test = ["LOL", "THIS", "IS", "A", "TEST1", "TEST2", "TEST3", "TEST4"];

    $( "#search_input" ).autocomplete({
            source: function(req, responseFn) {
		var re = $.ui.autocomplete.escapeRegex(req.term);
		var matcher = new RegExp( "^" + re, "i" );
		var a = $.grep(test, function(item,index){
			return matcher.test(item);
		    });
		responseFn( a );
	    }
	    /**source: availableTags**/
	});

      });
    });
