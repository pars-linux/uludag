{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari}}
<table border=1 width=20% align=center cellpadding=10> 
 <form action="{{$Burasi}}" method="POST">
 <tr>
  <td><b>Anasayfa:</td>
  <td>
    <select name="AnaSayfa" onchange="this.form.submit();" size=10>
      {{html_options options=$AnaSayfalar selected=$SeciliAnaSayfa}}
    </select>
  </td>
 </tr>
 </form>
 {{if $AltSayfalar}}
  <tr>
   <td colspan=2>
     <table border=1 width=100% cellpadding=5>
      <tr><td><b>Menüdeki Sayfalar</b></td></tr>  
      {{foreach item=AltSayfa from=$AltSayfalar}}
         <tr> 
            <td>
              <a href="javascript:OzelPencere('{{$ASSayfa}}YonetimMenuDuzenle&SayfaNo={{$AltSayfa.No}}','OzelPencere',600,600,1,1)">{{$AltSayfa.Isim}}</a>
            </td>
         </tr>
      {{/foreach}}
     </table>
   </td>
  </tr>
 {{/if}}
</table>
<br><br>
{{if $smarty.post.AnaSayfa}}
  <table border=1 width=30% align=center cellpadding=5>
   <form action="{{$Burasi}}" method="POST" onsubmit="return kontrol(this)">
   <tr><td colspan=2><b>{{$SayfaIsim}}</b> menüsüne yeni sayfa ekle</td></tr>
   <tr>
    <td>Menü ismi :</td>
    <td><input type="text" name="N_MenuIsim" alt="Menü ismi"></td>
   </tr>
   <tr>
    <td>Kaynak Dosya Ýsmi :</td>
    <td><input type="text" name="N_KaynakIsim" alt="Kaynak dosya ismi"></td>
   </tr>
   <input type=hidden name="AnaSayfa" value="{{$SeciliAnaSayfa}}">
   <tr><td colspan=2 align=right><input type="submit" name="Ekle" value="Ekle" class=onay></td></tr>
  </form>
  </table>

{{/if}}
{{/strip}}
