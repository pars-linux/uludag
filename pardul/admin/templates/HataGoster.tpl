{{strip}}

{{if $YetkiHataMesaj}}
<div id="YetkiHataMesajDiv" style="display:block; position:absolute; top:1; left;350; border:solid; border-width:1px; border-color:red; z-index:0; background-color:#f4f4f4; height:150px; width:400px; overflow:auto;" ondblclick="document.getElementById('YetkiHataMesajDiv').style.display='none';">
<table width=100% align=center border=0 cellpadding=5 height="100%">
 <tr><td valign=top><img src="{{$WebAdminResimler}}/uyari.png"></td><td class=uyari align="center">{{$YetkiHataMesaj}} iþlemini gerçekleþtirme yetkiniz yoktur !<td valign="top"><img src="{{$WebAdminResimler}}/takvim_close.gif" onClick="document.getElementById('YetkiHataMesajDiv').style.display='none';"></td></tr>
</table>
</div>
{{/if}}

{{if $Uyari}}
<div id="UyariMesajDiv" style="display:block; position:absolute; top:1; left;350; border:solid; border-width:1px; border-color:#007000; z-index:0; background-color:#f4f4f4; height:150px; width:400px; overflow:auto;" ondblclick="document.getElementById('UyariMesajDiv').style.display='none';">
<table width=100% border=0 height="100%" cellpadding="5">
 {{foreach item=Uyari from=$Uyari}}
  <tr><td valign="top"><img src="{{$WebAdminResimler}}/uyari.png"></td><td class=uyari align="center">{{$Uyari}}</td><td valign="top"><img src="{{$WebAdminResimler}}/takvim_close.gif" onClick="document.getElementById('UyariMesajDiv').style.display='none';"></td></tr>
 {{/foreach}}
</table>
</div>
{{/if}}
{{/strip}}
