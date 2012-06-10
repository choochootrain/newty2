(function($){
                    $.fn.preventUglyScroll = function(){
                    
                        var node = this[0];
                    
                        node.ontouchstart = function(event) {
                            touchStart = event;
                            frameStart = $(node).offset().top;
                        }
                        
                        node.ontouchmove = function(event){
    
                            // block all two finger gestures
                            if(event.touches.length > 1) {
                                event.preventDefault();
                                return false;
                            }
    
                            event.preventDefault();
                            
                            var yDiff     = event.pageY - touchStart.pageY;
                            var newTop  = yDiff + frameStart;
                            var hMin     = 460 - $(node).height();
                            if(newTop <= 0 && newTop > hMin) {
                                $(node).css('margin-top', newTop);
                            }
                        }
                    }
                })($);
