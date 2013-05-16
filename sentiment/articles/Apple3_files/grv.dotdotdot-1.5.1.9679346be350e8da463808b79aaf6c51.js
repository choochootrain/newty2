/*
 *	jQuery dotdotdot 1.5.1
 *
 *	Copyright (c) 2012 Fred Heusschen
 *	www.frebsite.nl
 *
 *	Plugin website:
 *	dotdotdot.frebsite.nl
 *
 *	Dual licensed under the MIT and GPL licenses.
 *	http://en.wikipedia.org/wiki/MIT_License
 *	http://en.wikipedia.org/wiki/GNU_General_Public_License
 */

(function(g){function u(a,e,c,j,f){var i=a.contents(),b=!1;a.empty();for(var h=0,k=i.length;h<k&&!b;h++){var d=i[h],m=g(d);if("undefined"!=typeof d){a.append(m);if(f){var q=a.is("table, thead, tbody, tfoot, tr, col, colgroup, object, embed, param, ol, ul, dl, select, optgroup, option, textarea, script, style")?"after":"append";a[q](f)}3==d.nodeType?c.innerHeight()>j.maxHeight&&(b=s(m,e,c,j,f)):b=u(m,e,c,j,f);b||f&&f.remove()}}return b}function s(a,e,c,j,f){var i=!1,b=a[0];if("undefined"==typeof b)return!1;
for(var i="letter"==j.wrap?"":" ",h=(b.innerText?b.innerText:b.nodeValue?b.nodeValue:b.textContent?b.textContent:"").split(i),k=-1,d=-1,m=0,q=h.length-1;m<=q;){var v=Math.floor((m+q)/2);if(v==d)break;d=v;r(b,h.slice(0,d+1).join(i)+j.ellipsis);c.innerHeight()>j.maxHeight?q=d:m=k=d}if(-1!=k){a=h.slice(0,k+1).join(i);for(i=!0;-1<g.inArray(a.slice(-1),j.lastCharacter.remove);)a=a.slice(0,-1);0>g.inArray(a.slice(-1),j.lastCharacter.noEllipsis)&&(a+=j.ellipsis);r(b,a)}else b=a.parent(),a.remove(),$n=b.contents().eq(-1),
i=s($n,e,c,j,f);return i}function n(a){return{width:a.innerWidth(),height:a.innerHeight()}}function r(a,g){a.innerText?a.innerText=g:a.nodeValue?a.nodeValue=g:a.textContent&&(a.textContent=g)}if(!g.fn.dotdotdot){g.fn.dotdotdot=function(a){if(0==this.length){var e='No element found for "'+this.selector+'".',e="string"==typeof e?"dotdotdot: "+e:["dotdotdot:",e];window.console&&window.console.log&&window.console.log(e);return this}if(1<this.length)return this.each(function(){g(this).dotdotdot(a)});var c=
this;c.data("dotdotdot")&&c.trigger("destroy.dot");c.bind_events=function(){c.bind("update.dot",function(a,d){a.preventDefault();a.stopPropagation();var b=f,e;if("number"==typeof f.height)e=f.height;else{e=c.innerHeight();var h=["paddingTop","paddingBottom"];z=0;for(l=h.length;z<l;z++){var p=parseInt(c.css(h[z]),10);isNaN(p)&&(p=0);e-=p}}b.maxHeight=e;f.maxHeight+=f.tolerance;if("undefined"!=typeof d){if("string"==typeof d||d instanceof HTMLElement)d=g("<div />").append(d).contents();d instanceof
g&&(j=d)}k=c.wrapInner('<div class="dotdotdot" />').children();k.empty().append(j.clone(!0)).css({height:"auto",width:"auto",border:"none",padding:0,margin:0});b=h=!1;i.afterElement&&(h=i.afterElement.clone(!0),i.afterElement.remove());if(k.innerHeight()>f.maxHeight)if("children"==f.wrap){b=k;e=f;var p=b.children(),n=!1;b.empty();for(var t=0,s=p.length;t<s;t++){var r=p.eq(t);b.append(r);h&&b.append(h);if(b.innerHeight()>e.maxHeight){r.remove();n=!0;break}else h&&h.remove()}b=n}else b=u(k,c,k,f,h);
k.replaceWith(k.contents());k=null;g.isFunction(f.callback)&&f.callback.call(c[0],b,j);return i.isTruncated=b}).bind("isTruncated.dot",function(a,b){a.preventDefault();a.stopPropagation();"function"==typeof b&&b.call(c[0],i.isTruncated);return i.isTruncated}).bind("originalContent.dot",function(a,b){a.preventDefault();a.stopPropagation();"function"==typeof b&&b.call(c[0],j);return j}).bind("destroy.dot",function(a){a.preventDefault();a.stopPropagation();c.unwatch().unbind_events().empty().append(j).data("dotdotdot",
!1)});return c};c.unbind_events=function(){c.unbind(".dot");return c};c.watch=function(){c.unwatch();if("window"==f.watch){var a=g(window),d=a.width(),e=a.height();a.bind("resize.dot"+i.dotId,function(){if(d!=a.width()||e!=a.height()||!f.windowResizeFix)d=a.width(),e=a.height(),h&&clearInterval(h),h=setTimeout(function(){c.trigger("update.dot")},10)})}else b=n(c),h=setInterval(function(){var a=n(c);if(b.width!=a.width||b.height!=a.height)c.trigger("update.dot"),b=n(c)},100);return c};c.unwatch=function(){g(window).unbind("resize.dot"+
i.dotId);h&&clearInterval(h);return c};var j=c.contents(),f=g.extend(!0,{},g.fn.dotdotdot.defaults,a),i={},b={},h=null,k=null,e=i,d;d=f.after;"undefined"==typeof d||!d?d=!1:"string"==typeof d?(d=g(d,c),d=d.length?d:!1):d="object"==typeof d?"undefined"==typeof d.jquery?!1:d:!1;e.afterElement=d;i.isTruncated=!1;i.dotId=y++;c.data("dotdotdot",!0).bind_events().trigger("update.dot");f.watch&&c.watch();return c};g.fn.dotdotdot.defaults={ellipsis:"... ",wrap:"word",lastCharacter:{remove:" ,;.!?".split(""),
noEllipsis:[]},tolerance:0,callback:null,after:null,height:null,watch:!1,windowResizeFix:!0,debug:!1};var y=1,w=g.fn.html;g.fn.html=function(a){return"undefined"!=typeof a?this.data("dotdotdot")&&"function"!=typeof a?this.trigger("update",[a]):w.call(this,a):w.call(this)};var x=g.fn.text;g.fn.text=function(a){if("undefined"!=typeof a){if(this.data("dotdotdot")){var e=g("<div />");e.text(a);a=e.html();e.remove();return this.trigger("update",[a])}return x.call(this,a)}return x.call(this)}}})($grv);