{{strip}}
{{include file="Header.tpl"}}
<script>
function SayfaGonder(No)
        {
        document.ListeForm.SayfaNo.value = No;
        document.ListeForm.submit();
        }

</script>
<center>

<table border=0 width=100% style="border-collapse:collapse" cellpadding=3>
<tr class=tabbas1><td height=33 colspan=4>FÝRMA ARAMA</td></tr>
<form method="POST" action="{{$Burasi}}" name="ListeForm">
<input type=hidden name=SayfaNo value=1>
<input type=hidden name=Ara value=1>
 <tr class=tabloliste1>
   <td class=tdbaslik>Ad Soyad </td>
   <td><input type="text" name="AdSoyad" size=20 value="{{$AdSoyad}}"></td>
   <td class=tdbaslik>E-Posta</td>
   <td><input type="text" name="EPosta" value="{{$EPosta}}"></td>
 </tr>

 <tr>
   <td class=tdbaslik>Ýl</td>
   <td>
     <select name="Vilayet">
       {{html_options options=$Vilayetler selected=$Vilayet}}
     </select>
   </td>
   <td class=tdbaslik>Firma Ad</td>
   <td>
    	<input type="text" name="FirmaAd" value="{{$FirmaAd}}">
   </td>
 </tr>
 <tr><td colspan=4 align=right><input type="submit" name="Ara" value="Listele" class=onay></td></tr>
</table>
<br><br><br>
{{if $Uyeler}}

{{if $CokSayfali}}
<table width=90%>
        <tr><td colspan=4 align=right>
                <table><tr>
                {{if $OncekiSayfa}}
                <td align=center><a href="{{$OncekiSayfa}}"><b>Önceki</b></a></td>
                {{else}}
                <td align=center>Önceki</td>
                {{/if}}
                {{foreach item=K from=$SayfaKopruler}}
                    <td align=right><b>[{{if $K.Adres}}<a href="{{$K.Adres}}">{{$K.Isim}}</a>{{else}}{{$K.Isim}}{{/if}}]</td>
                {{/foreach}}
                {{if $SonrakiSayfa}}
                <td align=center><a href="{{$SonrakiSayfa}}"><b>Sonraki</a></td>
                {{else}}
                <td align=center>Sonraki</td>
                {{/if}}
                </tr></table>
        </td></tr>
</table>
{{/if}}

  <table border=0 width=100% cellpadding=4 style="border-collapse:collapse">
   <tr class=tabbas1>
    
      <td>Yetkili Ad Soyad</td>
      <td>Firma Ad</td>
      <td>Telefon</td>
      <td>Üyelik Tarih</td>
      <td>Ürün Ekle</td>
      <td>Ýþlem</td>
      
   </tr>
   {{foreach item=Uye from=$Uyeler name=Uye}}
   {{if $smarty.foreach.Uye.iteration is odd}}<tr class=tabloliste1> {{else}}<tr class=tabloliste2>{{/if}}
     
      <td>{{$Uye.AdSoyad}}</td>
      <td>{{$Uye.FirmaAd}}</td>
      <td>{{$Uye.Tel}}</td>
      <td>{{$Uye.UyelikTarih}}</td>
      <td align="center">
      <a href="javascript:OzelPencere('{{$ASSayfa}}BarkodBasvuruForm&UyeNo={{$Uye.No}}','UyeDuzenleme',700,500,1,1)"><img src="{{$WebAdminResimler}}/uyedetay.gif" border=0 alt="Düzenle"></a>&nbsp;
      </td>
      <td align=center>
        <a href="javascript:OzelPencere('{{$ASSayfa}}UyeDuzenle&UyeNo={{$Uye.No}}','UyeDuzenleme',700,500,0,1)"><img src="{{$WebAdminResimler}}/duzenle.gif" border=0 alt="Düzenle"></a>&nbsp;
        <a href="javascript:OzelPencere('{{$ASSayfa}}UyeYorum&UyeNo={{$Uye.No}}','UyeYorum',600,400,0,1)"><img src="{{$WebAdminResimler}}/defter.jpg" border=0 alt="{{$YorumAltCumle}}"></a>
      </td>
      
   </tr>
   {{/foreach}}
  </table>

{{else}}
{{if $Listelendi}}<center><b>Kayýt bulunamadý!</b></center>{{/if}}
{{/if}}
{{/strip}}
