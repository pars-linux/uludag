{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<table border=0 width=100% style="border-collapse:collapse" cellpadding=3 align=center>
<tr class=tabbas1><td colspan=4 height=33>ÜYE GÖRÜÞ VE ÖNERÝLERÝ</td></tr>
<form method="POST" action="{{$Burasi}}" name="ListeForm">
<input type=hidden name=SayfaNo value=1>
<input type=hidden name=Ara value=1>
 <tr class=tabloliste1>
   <td class=tdbaslik>Ad Soyad </td>
   <td><input type="text" name="AdSoyad" size=20 value="{{$AdSoyad}}"></td>
   <td class=tdbaslik>E-Posta </td>
   <td><input type="text" name="EPosta" value="{{$EPosta}}"></td>
 </tr>
 <tr>
 <td class=tdbaslik>Cevap Durum </td>
 <td>
  <select name="CevapDurum">
      <option value="">Tümü</option>
      <option value="Cevaplandi" {{if $CevapDurum eq 'Cevaplandi'}}selected{{/if}}>Cevaplanan</option>
      <option value="Cevaplanmadi" {{if $CevapDurum eq 'Cevaplanmadi'}}selected{{/if}}>Cevaplanmayan</option>
     </select>
 </td>
 <td class=tdbaslik>Durum </td>
 <td>
  <select name="AktifPasif">
      <option value="Tumu">Tümü</option>
      <option value="Aktif" {{if $AktifPasif eq 'Aktif'}}selected{{/if}}>Aktif</option>
      <option value="Pasif" {{if $AktifPasif eq 'Pasif'}}selected{{/if}}>Pasif</option>
     </select>
 </td>
 <tr><td colspan=4 align=right><input type="submit" name="Ara" value="Listele" class=onay></td></tr>
</form>
 </table>
<br><br>
{{if $Dizi}}
<table border=0 width=100% cellpadding=3 style="border-collapse:collapse">
<script language="Javascript">
function SayfaGonder(No)
	{
	document.ListeForm.SayfaNo.value = No;
	document.ListeForm.submit();
	}
</script>
<br><br>
<tr><br><td colspan="7" align="center">
 {{include file="SayfaLinkler.tpl"
           OncekiSayfa=$OncekiSayfa
           SonrakiSayfa=$SonrakiSayfa
           SayfaKopruler=$SayfaKopruler
         }}

<br>
</td>
<td colspan=7 align=left>Toplam <b>{{$TumSayi}}/{{$KayitSayi}}</b> kayýt listelenmiþtir</td>
</tr>
<tr class="tabbas1">
  <td>No</td>
  <td>Ad Soyad</td>
  <td>EPosta</td>
  <td>Mesaj</td>
  <td>Tarih</td>
  <td>Durum</td>
  <td>Oku-Cevapla</td>
  <td>Ýþlem</td>
</tr>

{{foreach item=Dizi from=$Dizi name=Dizi}}
 {{if $smarty.foreach.Dizi.iteration is odd}}<tr class="tabloliste1">{{else}}<tr class="tabloliste2">{{/if}}
  <td>{{$Dizi.No}}</td>
  <td>{{$Dizi.AdSoyad}}</td>
  <td>{{$Dizi.EPosta}}</td>
  <td>{{$Dizi.Mesaj}}</td>
  <td>{{$Dizi.TarihSaat}}</td>
  <td>{{$Dizi.CevapDurum}}</td>
  <td align=center><a href="javascript:OzelPencere('{{$ASSayfa}}UyeGorusOkuCevapla&No={{$Dizi.No}}','Oku',500,400,1,1)"><img src="{{$WebAdminResimler}}/duzenle.gif" border=0></a></td>
 <td align=center><a onclick="return confirm('Yorumu pasif yapmak istediðinize emin misiniz?')" href="{{$Burasi}}&Sil={{$Dizi.No}}"><img src="{{$WebAdminResimler}}/sil.gif" border=0 alt="Yorumu pasif yapmak için týklayýnýz. "></a></td>
 </tr>
{{/foreach}}
</table>
{{else}}
	<br><br><center class=uyari>Kayýt bulunamadý!</center>
{{/if}}
{{/strip}}
