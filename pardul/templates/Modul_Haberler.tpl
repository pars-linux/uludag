{{strip}}
{{include file="ModulTop.tpl" bgcolor="$sistem_Modul_Haberler"}}
<table border=0 width=94% cellpadding=3 align=center>
<tr><TD class="ModulBaslik">{{t}}Haberler{{/t}}</TD></tr>
 <tr><td>
{{if $HaberListe}}
 {{foreach item=Haber from=$HaberListe name=Haber}}
  <tr>
    <td>
    &#187; <a href="{{$SSayfa}}Haberler&HaberNo={{$Haber.No}}">{{$Haber.Baslik}}</a>
    </td>
  </tr>
 {{/foreach}}
  <tr>
   <td align="right"><hr><a href="{{$SSayfa}}DigerHaberler&Diger={{$Haber.No}}">{{t}}Diðer Haberler...{{/t}}</a></td>
  </tr>
{{else}}
  <tr><td align=center><b>{{t}}Kayýtlý Haber bulunmamaktadýr.{{/t}}</b></td></tr>
{{/if}}
</table>
{{include file="ModulFoot.tpl"}}
{{/strip}}
