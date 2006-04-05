{include file="head.mt"}
<div class="menu"><a href="?quit">Exit</a> &#8226; <a href="javascript:win.show();">Page List</a> &#8226; <a href="javascript:hola();">ist</a></div>
<div id="loginbox">

    {literal}

    <script>
    win = new Window('dialog', {className: "dialog", right:30, width:160, height:130, zIndex: 100, resizable: false, title: "Page List", hideEffect: Effect.SwitchOff})
    win.getContent().innerHTML= 
    "{/literal}<div style='padding:8px;'><b>Const Pages</b><br><li><a href=?edit=1>Main Page</a><br>{section name=node loop=$PageList}<a href=?edit={$PageList[node].ID}>{$PageList[node].PageTitle}</a><br>{/section}</div>{literal}"
    win.show();

    help = new Window('help', {className: "dialog", width:220, height:100, zIndex: 100, resizable: false, title: "Help", hideEffect: Effect.SwitchOff})
    help.getContent().innerHTML= "<b> Header of Page </b><br>This will be the link of page, do not use any sepcial character or space !"

    </script>

    <script type="text/javascript" src="commonlib/php/FCKeditor/fckeditor.js"></script>
    <script type="text/javascript">
        
      window.onload = function()
      {
        var oFCKeditor = new FCKeditor( 'hede' ) ;
        oFCKeditor.BasePath = "commonlib/php/FCKeditor/" ;
        oFCKeditor.Value = "memeooo";
        oFCKeditor.ReplaceTextarea();
      }
    </script>

<script>

    
    function hola(){
    
//     var fck = document.getElementById('maWeFCKeditor');
    var fck2 = document.getElementById('hede');
//         fck.value = "kokok";
//         alert (fck.value);
        fck2.value = "memeooo";
        
        alert (fck2.value);
        
    }
    document.onload= hola;
</script>
    {/literal}
    <form action="login.php" method="post">
    <fieldset id="maWeMain" style="width: 740px;">
        <legend>and the editor redesigned ..</legend>
            <span style="float:left;">
                <label for ="maWeTitle">Header of Page : </label>
                <input type="text" name="maWeTitle" value="{$PageTitle}" />
                <a href="javascript:help.showCenter();"><img src="{$maWe.Path}images/help.png" /></a>
            </span>
            <span style="float: right;margin-right:1px;">
                <input type="submit" name="maWeDoDoc" value="Update" />
            </span>
<!--         {$FCK} -->
        <textarea id="hede" name="hede"></textarea>
    </fieldset>
    </form>

</div>
</center>
</body>
</html>
