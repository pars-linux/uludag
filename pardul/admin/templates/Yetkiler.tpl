{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}

<center>
<table border=0 cellpadding=5 style="border-collapse:collapse;border-color:#000000" >
<form action="{{$Burasi}}" method=POST>
<tr class=tabbas1><td colspan=2>YÖNETÝCÝ BÝLGÝLERÝ</td></tr>
 <tr class=tabloliste1><td><b>Kullanici Ad :</b></td><td>{{$KullaniciAd}}</td></tr>
 <tr><td><b>Ad Soyad :</b></td><td><input type="text" name="AdSoyad" value="{{$AdSoyad}}" size=30></td></tr>
 <tr class=tabloliste1><td><b>Þifre :</b></td><td><input type="password" name="Sifre" value="{{$Sifre}}" size=30></td></tr>
 <tr><td><b>Tam Yetkili</b></td><td><input type="checkbox" name="TamYetki" {{if $TamYetki}}checked{{/if}}></td></tr>
 <tr><td colspan=2 align=right><input type=submit name="BilgiGuncelle" value="Güncelle" class="onay"></td></tr>
 <input type=hidden name=KullaniciAd value="{{$KullaniciAd}}">
</form>
</table>
</center>
<br><br>

<table border=0 width=50% cellpadding=5 align=center>
<form action="{{$Burasi}}" method=POST>
<tr class=tabbas1><td colspan=2>YETKÝ DÜZENLEME&nbsp;&nbsp; -&nbsp; Kullanici Ad: {{$KullaniciAd}}</td></tr>
{{foreach item=AnaSayfa from=$AnaSayfalar}}
 <tr class=tabbas3>
   <td width=3% align=center bgcolor=#990000></td>
   <td><label for="AnaSayfa{{$AnaSayfa.No}}">{{$AnaSayfa.Isim}}</label></td>
 </tr>
 {{if $AnaSayfa.AltSayfalar}}
  {{foreach item=AltSayfa from=$AnaSayfa.AltSayfalar name=AltSayfa}}
  {{if $smarty.foreach.AltSayfa.iteration is odd}} {{assign var=class value=tabloliste1}} {{else}} {{assign var=class value=tabloliste2}} {{/if}}
  <tr>
    <td width=5%>&nbsp;</td> 
    <td align=left>
      <table border=0 width=100%> 
       <tr class="{{$class}}">
         <td width=5% align=left><input name="Yetki{{$AltSayfa.No}}" {{if $AltSayfa.YetkiVar}} checked {{/if}} type=checkbox id="AltSayfa{{$AltSayfa.No}}"></td>
         <td>
           <label for="AltSayfa{{$AltSayfa.No}}">
             <b>{{if $AltSayfa.YetkiSayi}}<a href="javascript:OzelPencere('{{$ASSayfa}}YetkiDuzenle&SayfaNo={{$AltSayfa.No}}&KullaniciAd={{$KullaniciAd}}','YetkiDuzenle',400,400,1,1)">{{$AltSayfa.Isim}}</a>{{else}} {{$AltSayfa.Isim}} {{/if}} </b>
           </label>
           {{if $AltSayfa.Aciklama}}({{$AltSayfa.Aciklama}}) {{/if}}
         </td>
       </tr> 
      </table>
   {{if $AltSayfa.YeniPencereler}}
      <table border=0 width=100%> 
    {{foreach item=YeniPencere from=$AltSayfa.YeniPencereler}}
      <tr class="{{$class}}">
       <td width=10% align=right><input name="Yetki{{$YeniPencere.No}}" {{if $YeniPencere.YetkiVar}} checked {{/if}} type=checkbox id="YeniPencere{{$YeniPencere.No}}"></td>
       <td>
          <label for="YeniPencere{{$YeniPencere.No}}"><b>
             {{if $YeniPencere.YetkiSayi}} <a href="javascript:OzelPencere('{{$ASSayfa}}YetkiDuzenle&SayfaNo={{$YeniPencere.No}}&KullaniciAd={{$KullaniciAd}}','YetkiDuzenle',400,400,1,1)">{{$YeniPencere.Isim}}</a>{{else}} {{$YeniPencere.Isim}} {{/if}} </b>  
          </label>
           {{if $YeniPencere.Aciklama}}({{$YeniPencere.Aciklama}}) {{/if}}
       </td>
      </tr>
    {{/foreach}}
      </table>
   {{/if}}
   </td>
  </tr>
  {{/foreach}}
 {{/if}}
{{/foreach}}
<tr>
 <input type=hidden name="KullaniciAd" value="{{$KullaniciAd}}">
 <td colspan=2 align=right><input type="submit" name="Guncelle" value="Güncelle" class=onay></td>
</tr>
</form>
</table>
{{/strip}}
