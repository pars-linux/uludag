{{strip}}
<title>Üye Bilgileri Düzenleme</title>
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}

<center>
<table border=0 cellpadding=4 style="border-collapse:collapse" width="%100">
<form action="{{$Burasi}}" method="POST" onsubmit="javascript:return kontrol(this)">
 <tr class=tabbas1><td colspan=4>FÝRMA BÝLGÝLERÝ</td></tr>
 <tr class=tabloliste1>
   <td class=tdbaslik>Ad Soyad</td>
   <td><input type="text" name="N_AdSoyad" value="{{$Uye.AdSoyad}}" size=30></td>
 
   <td class=tdbaslik>E-Posta</td>
   <td><input type="text" name="N_EPosta1" value="{{$Uye.EPosta}}" size=30></td>
 </tr>
 <tr class=tabloliste1>
   <td class=tdbaslik>Firma Ad</td>
   <td><input type="text" name="N_FirmaAd" value="{{$Uye.FirmaAd}}" size=30></td>
 
   <td class=tdbaslik>Firma Unvan</td>
   <td><input type="text" name="N_FirmaUnvan" value="{{$Uye.FirmaUnvan}}" size=30></td>
 </tr>
 <tr class=tabloliste1>
   <td class=tdbaslik>Telefon</td>
   <td><input type="text" name="N_TelNo" value="{{$Uye.TelNo}}" size=30></td>
 
   <td class=tdbaslik>Faks</td>
   <td><input type="text" name="FaxNo" value="{{$Uye.FaxNo}}" size=30></td>
 </tr>
 <tr>
   <td class=tdbaslik valign="top">Adres</td>
   <td><textarea cols=40 rows=7 name="Adres">{{$Uye.Adres}}</textarea></td> 
   <td class=tdbaslik>Vilayet</td>
   <td>
     <select name="Vilayet">
       {{html_options options=$Vilayetler selected=$Uye.Vilayet}}
     </select>
   </td> 
 </tr>
 <tr colspan=2>
 <td class=tdbaslik>Dosya No</td>
   <td><input type="text" name="DosyaNo" value="{{$Uye.DosyaNo}}" size=17></td>
 </tr>
 
 <tr class=tabloliste1>
   <td class=tdbaslik>Tescil No</td>
   <td><input type="text" name="TescilNo" value="{{$Uye.TescilNo}}" size=30></td>
 
   <td class=tdbaslik>Vergi Numarasý</td>
   <td><input type="text" name="VergiNo" value="{{$Uye.VergiNo}}" size=30></td>
 </tr>
 <tr class=tabloliste1>
   <td class=tdbaslik>Vergi Dairesi</td>
   <td><input type="text" name="VergiDaire" value="{{$Uye.VergiDaire}}" size=30></td>
 
   <td class=tdbaslik>Web Adresi</td>
   <td><input type="text" name="WebAdres" value="{{$Uye.WebAdres}}" size=30></td>
 </tr>
 <tr class=tabloliste1>
   <td class=tdbaslik>Ürün Çeþit</td>
   <td><input type="text" name="N_UrunCesit" value="{{$Uye.UrunCesit}}" size=30></td>
 
   <td class=tdbaslik>EAN Tip</td>
   <td>
   		<select name="N_EANTip">
   			<option value="">Lütfen Seçiniz...
   			<option value="9" {{if $Uye.EANTip eq '9'}} selected {{/if}}>9 Basamaklý
   			<option value="8" {{if $Uye.EANTip eq '8'}} selected {{/if}}>8 Basamaklý
   			<option value="7" {{if $Uye.EANTip eq '7'}} selected {{/if}}>7 Basamaklý
   		</select>
   </td>
 </tr>
  <tr class=tabloliste1>
   <td class=tdbaslik colspan="2">MMNM Baþvuru Durumu</td>
   <td colspan="2"><input type="checkbox" name="MMNMBasvuru" {{if $Uye.MMNMBasvuru}} checked {{/if}}></td>
 </tr>
 
 
 <tr >
   <td class=tdbaslik>MMNM Vekalet</td>
   <td><input type="checkbox" name="MMNMVekalet" {{if $Uye.MMNMVekalet}} checked {{/if}}></td>
 
   <td class=tdbaslik>TOF Belge</td>
   <td><input type="checkbox" name="TOFBelge" {{if $Uye.TOFBelge}} checked {{/if}}></td>
 </tr>
 <tr>
   <td class=tdbaslik>Özel Vekalet</td>
   <td><input type="checkbox" name="OzelVekalet" {{if $Uye.OzelVekalet}} checked {{/if}}></td>
 
   <td class=tdbaslik>Gelir Tablosu</td>
   <td><input type="checkbox" name="GelirTablosu" {{if $Uye.GelirTablosu}} checked {{/if}}></td>
 </tr>  
 <tr>
   <td class=tdbaslik>Sicil Gazete</td>
   <td><input type="checkbox" name="SicilGazete" {{if $Uye.SicilGazete}} checked {{/if}}></td>
 
   <td class=tdbaslik>Haber listesi üyeliði</td>
   <td><input type="checkbox" name="HaberListe" {{if $Uye.HaberListe}} checked {{/if}}></td>
 </tr>
 <tr><td colspan=2 align=right><input type="submit" name="Guncelle" value="Güncelle" class=onay></td></tr>
 <input type="hidden" name="UyeNo" value="{{$Uye.No}}">
</form>
</table>
<center>

<br>
<table width=85% border=0>
 <tr>
  <td>
     <a href="{{$Burasi}}&Sil=1&UyeNo={{$Uye.No}}" title="Dikkat!!! Üyeyi silmek üzeresiniz." onclick="return confirm('Üyeyi SÝLMEK istediðinize emin misiniz?')"><img alt="Dikkat!!! Üyeyi silmek üzeresiniz." src="{{$WebAdminResimler}}/sil.gif" border=0>Üye Sil</a>
  </td>
  <td align=right>
     <a href="{{$Burasi}}&SifreGonder=1&UyeNo={{$Uye.No}}" title="Þifresini unutan kullanýcýya yeni þifre göndermek için kullanýlýr" onclick="return confirm('Üyeye YENÝ ÞÝFRE göndermek istediðinize emin misiniz?')">Yeni Þifre Gönder</a>
  </td>
 </tr> 
</table>
{{/strip}}
