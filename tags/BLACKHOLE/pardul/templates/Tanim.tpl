{{strip}}
{{include file="TableTop.tpl"  bgcolor="#FFFFFF"}}
{{if $Harfler}}
    <table border=0 width="100%">
    {{foreach item=Harfler from=$Harfler name=Harfler}}
     <tr>
      <td valign="top">
        <b>{{$Harfler.Kelime}}</b><hr><br><div align="justify">{{$Harfler.Aciklama}}</div>
      </td>
    {{/foreach}}
    </table>
{{/if}}
{{include file="TableFoot.tpl"}}
{{/strip}}