{{strip}}
<title>�ye Bilgileri D�zenleme</title>
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}

{{if $Mesaj}}
 <center><b>{{$Mesaj}}</b></center><br>
{{/if}}
<center>
<table border=0 cellpadding=4 style="border-collapse:collapse">
<form action="{{$Burasi}}" method="POST" onsubmit="javascript:return kontrol(this)">
 <tr class=tabbas1><td colspan=2>S�ZC�K B�LG�LER�</td></tr>
 <tr class=tabloliste1>
   <td class=tdbaslik>S�zc�k</td>
   <td><input type="text" name="N_Kelime" value="{{$Kelime}}" size=30></td>
 </tr>
 <tr>
   <td class=tdbaslik>A��klama</td>
   <td><textarea cols=50 rows=10 name="Aciklama">{{$Aciklama}}</textarea></td>
 </tr>
  <tr><td colspan=2 align=right><input type="submit" name="Guncelle" value="G�ncelle" class=onay></td></tr>
 <input type="hidden" name="No" value="{{$No}}">
</form>
</table>
{{include file="Footer.tpl"}}
<center>
{{/strip}}
