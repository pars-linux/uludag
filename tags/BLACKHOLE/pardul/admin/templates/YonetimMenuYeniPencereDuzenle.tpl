{{strip}}
{{include file="HataGoster.tpl" Uyari=$Uyari}}
<title>{{$SayfaIsim}}</title>
<table border=1 width=100% cellpadding=5>
<tr class=tabbas1><td colspan=2><b>{{$SayfaIsim}} - MEVCUT ��LEM KODLAR</b></td></tr>
<tr><td><b>��lem Kod</b></td><td><b>A��klama</b></td></tr>
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
 <tr><td colspan=2><b>Yeni i�lem kod ekle :</b></td></tr>
 <tr> 
   <td>��lem Kod:</td>
   <td><input type="text" name="N_IslemKod" alt="��lem Kod"></td>
 </tr>
 <tr>
   <td>A��klama:</td>
   <td><input type="text" name="N_Aciklama" alt="A��klama" size="30"></td>
 </tr>
 <tr>
  <input type="hidden" name="SayfaNo" value="{{$SayfaNo}}">
  <td colspan=2 align=right><input type="submit" name="IslemKodEkle" value="Ekle" class=onay></td>
 </tr>
 </form>
</table>
{{/strip}}
