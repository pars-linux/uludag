{{strip}}
{{include file="TableTop.tpl"  bgcolor="#FFFFFF"}}
<h1>S�k Sorulan Sorular</h1>
{{if $Cevap}}
<!-- Cevap k�sm� ba�lad� -->
<table border=0 cellpadding=5 style="border-collapse:collapse" width=95%>
 {{foreach item=Soru from=$Sorular}}
   <tr><td><h3>{{$Soru.Soru}}</h3></td></tr>
   <tr><td>{{$Soru.Cevap}}</td></tr>
 {{/foreach}}
</table><BR>
&nbsp;&nbsp;&#8249;&#8249;<a href="{{$SSayfa}}Sss">{{t}}GER�{{/t}}</A>
{{else}}
<br><br><br>
<!-- Kategoriler ve sorular ba�lad� -->
<table border=0 cellpadding=5 style="border-collapse:collapse" width="95%" align="center">
 {{foreach item=Kategori from=$Kategoriler}}
  <tr><td><h3>{{$Kategori.Ad}}</h3></td></tr>
  {{foreach item=Soru from=$Sorular}}
   {{if $Soru.KatNo==$Kategori.No}}
      <tr><td><li>
      <a href="{{$SSayfa}}Sss&SssNo={{$Soru.No}}">{{$Soru.Soru}}</a></td></tr>
   {{/if}}
  {{/foreach}}
 {{/foreach}}
</table><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
<!-- Kategoriler ve sorular bitti -->
{{/if}}
<!-- Cevap k�sm� bitti -->
{{include file="TableFoot.tpl"}}
{{/strip}}