var jcropapi;function setupJcrop(t,o,i,e){t.Jcrop({trueSize:[o.width,o.height],bgColor:"rgb(192, 192, 192)",onSelect:function(t){var o=Math.floor((t.x+t.x2)/2),i=Math.floor((t.y+t.y2)/2),a=Math.floor(t.w),h=Math.floor(t.h);e.x.val(o),e.y.val(i),e.width.val(a),e.height.val(h)},onRelease:function(){e.x.val(i.x),e.y.val(i.y),e.width.val(i.width),e.height.val(i.height)}},(function(){jcropapi=this,$("img",this.ui.holder).attr("alt","");const t=i.label;if(!t)return;const o="jcrop-holder-input";$("input",this.ui.holder).attr("id",o);const e=document.createElement("label");e.setAttribute("for",o),e.classList.add("w-sr-only"),e.textContent=t,document.getElementsByClassName("jcrop-holder")[0].prepend(e)}))}$((function(){var t=$("div.focal-point-chooser"),o=$(".current-focal-point-indicator",t),i=$("img",t),e={width:i.data("originalWidth"),height:i.data("originalHeight")},a={label:t.data("focalInputLabel"),x:t.data("focalPointX"),y:t.data("focalPointY"),width:t.data("focalPointWidth"),height:t.data("focalPointHeight")},h={x:$("input.focal_point_x"),y:$("input.focal_point_y"),width:$("input.focal_point_width"),height:$("input.focal_point_height")},l=a.x-a.width/2,r=a.y-a.height/2,n=a.width,c=a.height;o.css("left",100*l/e.width+"%"),o.css("top",100*r/e.height+"%"),o.css("width",100*n/e.width+"%"),o.css("height",100*c/e.height+"%");var p=[i,e,a,h];setupJcrop.apply(this,p),$(window).on("resize",$.debounce(300,(function(){jcropapi.destroy(),i.removeAttr("style"),$(".jcrop-holder").remove(),setupJcrop.apply(this,p)}))),$(".remove-focal-point").on("click",(function(){jcropapi.destroy(),i.removeAttr("style"),$(".jcrop-holder").remove(),$(".current-focal-point-indicator").remove(),h.x.val(""),h.y.val(""),h.width.val(""),h.height.val(""),setupJcrop.apply(this,p)}))}));