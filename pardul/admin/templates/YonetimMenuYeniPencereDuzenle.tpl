{{strip}}
{{include file="HataGoster.tpl" Uyari=$Uyari}}
<title>{{$SayfaIsim}}</title>
<table border=1 width=100% cellpadding=5>
<tr class=tabbas1><td colspan=2><b>{{$SayfaIsim}} - MEVCUT ÝÞLEM KODLAR</b></td></tr>
<tr><td><b>Ýþlem Kod</b></td><td><b>Açýklama</b></td></tr>
{{foreach item=AltYetki from=$AltYetkiler}}
 <tr>
   <td>{{$AltYetki.IslemKod}}</td>
   <td>{{$AltYetki.Aciklama}}</td>
 </tr>
{{/foreach}}
</table>
<br>
<table border=1 width=100% cellpadding=3>
 <form action="{{$Burasi}}" method="POST" onsubmit="return kontrol(this);"> 
 <tr><td colspan=2><b>Yeni iþlem kod ekle :</b></td></tr>
 <tr> 
   <td>Ýþlem Kod:</td>
   <td><input type="text" name="N_IslemKod" alt="Ýþlem Kod"></td>
 </tr>
 <tr>
   <td>Açýklama:</td>
   <td><input type="text" name="N_Aciklama" alt="Açýklama" size="30"></td>
 </tr>
 <tr>
  <input type="hidden" name="SayfaNo" value="{{$SayfaNo}}">
  <td colspan=2 align=right><input type="submit" name="IslemKodEkle" value="Ekle" class=onay></td>
 </tr>
 </form>
</table>
{{/strip}}
