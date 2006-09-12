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
