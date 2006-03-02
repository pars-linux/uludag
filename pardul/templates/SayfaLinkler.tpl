{{strip}}
<table border=0>
<tr>
{{if $OncekiSayfa}}
  <td align=center><a href="{{$OncekiSayfa}}">{{t}}Önceki{{/t}}</a></td>
{{else}}
  <td align=center>{{t}}Önceki{{/t}}</td>
{{/if}}
{{foreach item=K from=$SayfaKopruler}}
   <td align=right>[{{if $K.Adres}}<a href="{{$K.Adres}}">{{$K.Isim}}</a>{{else}}{{$K.Isim}}{{/if}}]</td>
{{/foreach}}
{{if $SonrakiSayfa}}
   <td align=center><a href="{{$SonrakiSayfa}}">{{t}}Sonraki{{/t}}</a></td>
{{else}}
<td align=center>{{t}}Sonraki{{/t}}</td>
{{/if}}
</tr>
</table>
{{/strip}}
