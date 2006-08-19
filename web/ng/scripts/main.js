        function get_news(nid) {
            var url ='news.php';
            var linke = 'NewsID='+nid;
            var AjaxPointer = new Ajax.Request(url,{method:'get', parameters: linke, onComplete: showit});
        }

        function showit(originalRequest){
            var newData = originalRequest.responseText;
            $('haber').innerHTML = "";
            $('haber').innerHTML = newData;
            new Effect.Highlight('haber',{startcolor:'#CCE0E6', endcolor:'#FFFFFF'});
            $('haber').style.background = "#FFF";
        }
