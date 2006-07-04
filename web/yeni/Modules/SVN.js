
        function GetLogs(Repo,Obj){
            $(Obj).className='working';
            $(Obj).innerHTML="";
            var BaseLink= "http://svn.pardus.org.tr/viewcvs?view=rev&root=%22"+Repo+"%22&revision=";
            var url = '../Modules/SVN.php?Repo='+Repo;
            var ajax = new Ajax.Updater(
                '',
                url,
                {
                    method:'get',
                    onComplete: function(req){
                        $(Obj).innerHTML="";
                        var node = req.responseXML;
                        var root = node.getElementsByTagName('log').item(0);
                        var limit = 5;
                        $(Obj).className='ready';
                        for (i=0;i<=limit;i++) {
                            rev = root.getElementsByTagName('logentry').item(i).getAttribute("revision");
                            hede = '<li><a href="'+BaseLink+rev+'">r'+rev+' : '+root.getElementsByTagName('author').item(i).textContent+"</a><br>";
                            $(Obj).innerHTML += hede;
                        }
                    }
                }
            );
        }
