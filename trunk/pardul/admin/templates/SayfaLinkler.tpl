{{strip}}
<table>
<tr>
{{if $OncekiSayfa}}
  <td align=center><a href="{{$OncekiSayfa}}">�nceki</a></td>
{{else}}
  <td align=center>�nceki</td>
{{/if}}
{{foreach item=K from=$SayfaKopruler}}
   <td align=right>[{{if $K.Adres}}<a href="{{$K.Adres}}">{{$K.Isim}}</a>{{else}}{{$K.Isim}}{{/if}}]</td>
{{/foreach}}
{{if $SonrakiSayfa}}
   <td align=center><a href="{{$SonrakiSayfa}}">Sonraki</a></td>
{{else}}
<td align=center>Sonraki</td>
{{/if}}
</tr>
</table>
{{/strip}}
