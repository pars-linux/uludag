{{strip}}
{{include file="Stil.tpl"}}
<title>Yard�m</title>
{{if $YardimVar}}
<table width=100% cellpadding=10>
 <tr>
   <td class=tabbas3><b>{{$SayfaAdi}}</b></td>
 </tr>
 <tr>
  <td class=tabbas2><br>{{$YazilacakMetin}}<br><br></td>
 </tr>
</table>
{{else}}
  <br><br><center><b>Yardim d�k�man� bulunamad�!</b></center>
{{/if}}

<br>
<table width=100%>
<form action="{{$Burasi}}" method="POST">
<tr>
 <td><textarea name="YeniMetin" cols=73 rows=25>{{$Metin}}</textarea></td>
</tr>
<tr>
<td align=right>
 <input type="hidden" name="Sayfa" value="{{$Sayfa}}">
 <input type="submit" name="Guncelle" value="G�ncelle">
</td>
</tr>
</form>
</table>
<br>
<table width=100%>
 <tr>
  <td align=center>
    [ <a href="Javascript:window.close();">Kapat</a> ]
  </td>
 </tr>
</table>
{{/strip}}
