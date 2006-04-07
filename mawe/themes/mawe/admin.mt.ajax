{include file="head.mt"}
<div class="menu"><a href="?quit">Exit</a> &#8226; <a href="javascript:win.show();">Page List</a>&#8226; <a href="javascript:SetContents();">PList</a></div>
<div id="loginbox">

    {literal}

    <script>
    win = new Window('dialog', {className: "dialog", right:30, width:160, height:130, zIndex: 100, resizable: false, title: "Page List", hideEffect: Effect.SwitchOff})
    win.getContent().innerHTML= 
    "{/literal}<div style='padding:8px;'><b>Pages</b><br><li>{section name=node loop=$PageList}<a href=?edit={$PageList[node].ID}>{$PageList[node].PageTitle}</a><br>{/section}</div>{literal}"
    win.show();

    help = new Window('help', {className: "dialog", width:220, height:100, zIndex: 100, resizable: false, title: "Help", hideEffect: Effect.SwitchOff})
    help.getContent().innerHTML= "<b> Header of Page </b><br>This will be the link of page, do not use any sepcial character or space !"

    </script>

    {/literal}

    {literal}

        <script src="commonlib/php/FCKeditor/fckeditor.js"></script>
        <script>

        function update_page() {
            var oEditor = FCKeditorAPI.GetInstance('maWeFCKeditor');
            var PageBody= escape(oEditor.GetXHTML());
            var linke='title='+$('maWePageTitle').value+'&body='+PageBody+'&id='+$('maWePageID').value;
            var url ='do.php';
            var myAjax = new Ajax.Request(url,{method:'post', parameters: linke, onComplete: showit});
        }

        function showit(originalRequest){
            var newData = originalRequest.responseText;
            info = new Window('info', {className: "dialog", width:200, height:70, zIndex: 100, resizable: false, title: "Info", hideEffect: Effect.SwitchOff})
            info.getContent().innerHTML= newData
            info.showCenter();
        }

        </script>

        {/literal}

    <div class="dropmenu" id="dropmen">
        <div id="infos"></div>
    </div>
    <fieldset id="maWeMain" style="width: 740px;">
        <legend>and the editor redesigned ..</legend>
            <span style="float:left;">
                <label for ="maWeTitle">Header of Page : </label>
                <input type="text" name="maWePageTitle" id="maWePageTitle" value="{$PageTitle}" />
                <input type="hidden" name="maWePageID" id="maWePageID" value="{$PageID}" />
                <a href="javascript:help.showCenter();"><img src="{$maWe.Path}images/help.png" /></a>
            </span>
            <span style="float: right;margin-right:1px;">
                <input type="submit" name="maWeDoDoc" id="maWeDoDoc" value="Update" onclick="update_page();" />
            </span>
         {$FCK}
    </fieldset>

</div>
</center>
</body>
</html>
