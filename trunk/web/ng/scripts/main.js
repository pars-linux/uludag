        function get_news(nid) {
            var url ='news.php';
            var linke = 'NewsID='+nid;
            var AjaxPointer = new Ajax.Request(url,{method:'get', parameters: linke, onComplete: showit});
        }

        function showit(originalRequest){
            var newData = originalRequest.responseText;
            $('haber').innerHTML = "";
            $('haber').innerHTML = newData;
            new Effect.Highlight('haber',{startcolor:'#3991C0', endcolor:'#E8F2F4'});
            $('haber').style.background = "#E8F2F4";
        }

        function get_url(linker,diver) {
            var AjaxP = new Ajax.Request(linker,{method:'get', parameters:'', onComplete: function(response,diver){$(diver).innerHTML = response.responseText;}});
        }

        function startList() {
        //code only for IE
            //if(!document.body.currentStyle) return;
            var subs = document.getElementsByName('pi');
            for(var i=0; i<subs.length; i++) {
                var li = subs[i].parentNode;
                if(li && li.lastChild.style) {
                    li.onmouseover = function() {
                        this.lastChild.style.visibility = 'visible';
                    }
                    li.onmouseout = function() {
                        this.lastChild.style.visibility = 'hidden';
                    }
                }
            }
        }
