{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<table border=0 width=100% cellpadding=1 cellspacing=0 align=left>
 <form action="{{$Burasi}}" method="POST">
 <tr class=tabbas1><td colspan=3>Y�NET�M MEN� �ZELL�KLER�</td></tr>
 <tr class=tabbas2><td width=40%>&nbsp;</td><td>�zellik</td><td>De�er</td></tr>
 {{foreach item=Ozellik from=$Degiskenler}}
 <tr>
   <td></td>
   <td>{{$Ozellik.Isim}}</td>
   <td align=center><input type="text" name="{{$Ozellik.Isim}}" value="{{$Ozellik.Deger}}" size=30></td>
 </tr>
 {{/foreach}}
 <tr><td colspan=3 align=right><input type=submit name="Guncelle" value="G�ncelle" class=onay></td></tr>
 </form>
</table>
{{/strip}}
