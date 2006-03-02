{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<SCRIPT language="javascript">
 function SifreKontrol()
  {
    var sifre=document.EkleForm.N_Sifre.value;
    if((sifre.length<6)&&(sifre!=''))
    {
       alert('Þifreniz en az 6 haneli olmalýdýr!');
       return false;
    }

    if(document.EkleForm.N_Sifre.value != document.EkleForm.N_SifreTekrar.value)
     {
      alert("Þifreleriniz Uyuþmamakta!");
      return false;
     }
     else return true;
  }
</SCRIPT>
<center>
<table border=0 width=100% cellpadding=5>
  <tr class=tabbas1><td colspan=5>KAYITLI YÖNETÝCÝLER</td></tr>
  <tr class=tabbas2>
   <td>Kullanýcý Ad</td>
   <td>Ad Soyad</td>
   <td align=center>Durum</td>
   <td align=center>Ýþlem</td>
   <td>&nbsp;</td>
  </tr>
  {{foreach item=Yonetici from=$Yoneticiler name=Yoneticiler}}
  {{if $smarty.foreach.Yoneticiler.iteration is odd}}<tr class=tabloliste1> {{else}} <tr class=tabloliste2>{{/if}}
   <form action="{{$Burasi}}" method="POST">
   <td><b>{{$Yonetici.KullaniciAd}}</b></td>
   <td>{{$Yonetici.AdSoyad}}</td>
   <td align=center><b>{{$Yonetici.Durum}}</b></td>
   <td align=center><input type="submit" name="Degistir" value="{{$Yonetici.OlacakDurum}} Yap"></td>
   <input type="hidden" name="YeniDurum" value="{{$Yonetici.OlacakDurum}}">
   <input type="hidden" name="KullaniciAd" value="{{$Yonetici.KullaniciAd}}">
   <td align=center><a href="{{$ASSayfa}}Yetkiler&KullaniciAd={{$Yonetici.KullaniciAd}}"><img alt="Yetkileri düzenle..." src="{{$WebAdminResimler}}/duzenle.gif" border=0></a></td>
   </form>
  </tr>
  {{/foreach}} 
</table>
<br><br>
<table border=0 width=50% cellpadding=5>
<form action="{{$Burasi}}" method="POST" name="EkleForm" onsubmit="if (SifreKontrol()) return kontrol(this); else return false;">
 <tr><td colspan=2 class=tabbas1>YENÝ YÖNETÝCÝ EKLEME</td></tr>
 <tr class=tabloliste1><td width=30%><b>Kullanýcý Ad :</b></td><td><input type="text" name="N_YeniKullaniciAd" alt="Kullanýcý Ad"></td></tr>
 <tr><td><b>Kullanýcý Ad Soyad :</b></td><td><input type="text" name="N_YeniKullaniciAdSoyad" alt="Kullanýcý Ad Soyad"></td></tr>
 <tr class=tabloliste1><td><b>Þifre :</b></td><td><input type="password" name="N_Sifre" alt="Þifre"></td></tr>
 <tr><td><b>Þifre Tekrar :</b></td><td><input type="password" name="N_SifreTekrar" alt="Þifre Tekrar"></td></tr>
 <tr class=tabloliste1><td colspan=2 align=right><input type="submit" name="KullaniciEkle" value="Ekle" class=onay></td></tr>
</form>
</table>


</center>

{{/strip}}
