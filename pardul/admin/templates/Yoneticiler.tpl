{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<SCRIPT language="javascript">
 function SifreKontrol()
  {
    var sifre=document.EkleForm.N_Sifre.value;
    if((sifre.length<6)&&(sifre!=''))
    {
       alert('�ifreniz en az 6 haneli olmal�d�r!');
       return false;
    }

    if(document.EkleForm.N_Sifre.value != document.EkleForm.N_SifreTekrar.value)
     {
      alert("�ifreleriniz Uyu�mamakta!");
      return false;
     }
     else return true;
  }
</SCRIPT>
<center>
<table border=0 width=100% cellpadding=5>
  <tr class=tabbas1><td colspan=5>KAYITLI Y�NET�C�LER</td></tr>
  <tr class=tabbas2>
   <td>Kullan�c� Ad</td>
   <td>Ad Soyad</td>
   <td align=center>Durum</td>
   <td align=center>��lem</td>
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
   <td align=center><a href="{{$ASSayfa}}Yetkiler&KullaniciAd={{$Yonetici.KullaniciAd}}"><img alt="Yetkileri d�zenle..." src="{{$WebAdminResimler}}/duzenle.gif" border=0></a></td>
   </form>
  </tr>
  {{/foreach}} 
</table>
<br><br>
<table border=0 width=50% cellpadding=5>
<form action="{{$Burasi}}" method="POST" name="EkleForm" onsubmit="if (SifreKontrol()) return kontrol(this); else return false;">
 <tr><td colspan=2 class=tabbas1>YEN� Y�NET�C� EKLEME</td></tr>
 <tr class=tabloliste1><td width=30%><b>Kullan�c� Ad :</b></td><td><input type="text" name="N_YeniKullaniciAd" alt="Kullan�c� Ad"></td></tr>
 <tr><td><b>Kullan�c� Ad Soyad :</b></td><td><input type="text" name="N_YeniKullaniciAdSoyad" alt="Kullan�c� Ad Soyad"></td></tr>
 <tr class=tabloliste1><td><b>�ifre :</b></td><td><input type="password" name="N_Sifre" alt="�ifre"></td></tr>
 <tr><td><b>�ifre Tekrar :</b></td><td><input type="password" name="N_SifreTekrar" alt="�ifre Tekrar"></td></tr>
 <tr class=tabloliste1><td colspan=2 align=right><input type="submit" name="KullaniciEkle" value="Ekle" class=onay></td></tr>
</form>
</table>


</center>

{{/strip}}
