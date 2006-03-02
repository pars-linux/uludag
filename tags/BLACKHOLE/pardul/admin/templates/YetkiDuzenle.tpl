{{strip}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<title>Yetki Düzenleme</title>
<table border=1 width=100% cellpadding=3>
 <form action="{{$Burasi}}" method="POST">
 <tr><td colspan=3 class=tabbas1>{{$SayfaIsim}}</td></tr> 
 {{foreach item=Yetki from=$Yetkiler name=Yetkiler}}
  {{if $smarty.foreach.Yetkiler.iteration is odd}} <tr class=tabloliste1> {{else}}<tr class=tabloliste2> {{/if}}
   <td width=5%><input name="Yetki{{$Yetki.No}}" type="checkbox" {{if $Yetki.YetkiVar}} checked {{/if}} id="YetkiIsim{{$Yetki.No}}"></td>
   <td><label for="YetkiIsim{{$Yetki.No}}">{{$Yetki.Isim}}</label></td>
   <td>{{$Yetki.Aciklama}}</td>
  </tr>
 {{/foreach}}
   <input type=hidden name="SayfaNo" value="{{$SayfaNo}}">
   <input type=hidden name="KullaniciAd" value="{{$KullaniciAd}}">
   <tr><td colspan=3 align=right><input type="submit" name="Guncelle" value="Güncelle" class=onay></td></tr>
 </form>
</table>
{{include file="Footer.tpl"}}
{{/strip}}
