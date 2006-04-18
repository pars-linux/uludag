{include file="head.mt"}
<div class="menu"><a href="?quit">Exit</a> &#8226; <a href="javascript:ShowPageList();">Page List</a>&#8226;</div>
<div id="loginbox">

    {literal}

    <script>

    function ShowPageList() {
        win = new Window('dialog', {className: "dialog", right:30, width:160, height:400 , zIndex: 100, resizable: true, title: "the Menu", hideEffect: Effect.SwitchOff})
        win.getContent().innerHTML=
        "{/literal}<div style='padding:8px;'><a href='?new'><img src='{$maWe.Path}images/add.png' />Add New Page</a><br /><br /><b>Pages</b><br /><br /><div>{section name=node loop=$PageList}<span style='float:left;clear:left;'><img src='{$maWe.Path}images/page.png' /><a href=?edit={$PageList[node].ID}>{$PageList[node].PageTitle}</a></span><span style='float:right;'><img src='{$maWe.Path}images/delete.png' /></span><br>{/section}</div></div>{literal}"
        win.show();
    }

    function ShowHelp() {
        help = new Window('help', {className: "dialog", width:220, height:100, zIndex: 100, resizable: false, title: "Help", hideEffect: Effect.SwitchOff})
        help.getContent().innerHTML= "<b> Header of Page </b><br>This will be the link of page, do not use any sepcial character or space !"
        help.showCenter();
    }

    function ShowInfo() {
        info = new Window('info', {className: "dialog", width:200, height:10, zIndex: 100, resizable: false, title: "Info", hideEffect: Effect.SwitchOff})
        info.getContent().innerHTML= {/literal}{$OK}{literal}
        info.showCenter();
    }

    window.onload = ShowPageList;
    </script>

    {/literal}

    <fieldset id="maWeMain" style="width: 740px;">
        <legend>and the editor redesigned ..</legend>
        {if $OK}
        {literal}
        <script>
            ShowInfo();
        </script>
        {/literal}
        {/if}
        <form action="do.php" method="POST">
            <span style="float:left;">
                <label for ="maWeTitle">Header of Page : </label>
                <input type="text" name="maWePageTitle" id="maWePageTitle" value="{$PageTitle}" />
                <input type="hidden" name="maWePageID" id="maWePageID" value="{$PageID}" />
                <a href="javascript:ShowHelp();"><img src="{$maWe.Path}images/help.png" /></a>
            </span>
            <span style="float: right;margin-right:1px;">
                <input type="submit" name="maWeDoDoc" id="maWeDoDoc" value="{if $PageID==''}Add{else}Update{/if}" />
            </span>
         {$FCK}
        </form>
    </fieldset>

</div>
</center>
</body>
</html>
