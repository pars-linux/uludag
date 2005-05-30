{{strip}}
{{include file="ModulTop.tpl" bgcolor="$sistem_Modul_Sss"}}
<table width=100% border=0 cellpadding="0" cellspacing="0" style="border-collapse:collapse" align="center">
<tr><td class="ModulBaslik">{{t}}Sýk Sorulan Sorular{{/t}}</td></tr>
<tr>
<td>
<table border=0 width=100% cellpadding=3>
  {{foreach item=Soru from=$Sorular}}
      <tr>
        <td width="7" align="center" valign="middle"><img src="{{$WebResimler}}/plus.gif" align="top"></td>
        <td><a href="{{$SSayfa}}Sss#{{$Soru.No}}">{{$Soru.Soru}}</a></td>
      </tr>
  {{/foreach}}
</table></td>
</tr>
</table>
{{include file="ModulFoot.tpl"}}
{{/strip}}