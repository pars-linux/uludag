{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<table border=0 width=100% cellspacing=0 cellpadding=0>
    <tr class=tabbas1><td colspan=4>SIK SORULAN SORULAR KATEGORÝLERÝ</td></tr>
 <tr>
  <td width=30% valign=top>
   {{if $KategoriVar}}
   <table border=0 width=100% cellpadding=4 cellspacing=0>
    {{foreach item=SssKategori from=$SssKategoriler name=SssKategoriler}}
    {{if $smarty.foreach.SssKategoriler.iteration is odd}} <tr class=tabloliste1>{{else}} <tr class=tabloliste2>{{/if}}
       <td width=10%>
        {{if $SssKategori.Yukari}}
        <a href="{{$Burasi}}&Yukari=1&No={{$SssKategori.No}}"><img border=0 src="{{$WebAdminResimler}}/yukari.gif" alt="Yukarý">&nbsp;</a>
        {{/if}}
        {{if $SssKategori.Asagi}}
        <a href="{{$Burasi}}&Asagi=1&No={{$SssKategori.No}}"><img border=0 src="{{$WebAdminResimler}}/asagi.gif" alt="Aþagý"></a>
        {{/if}}
       </td>
       <td>
       <a href="{{$Burasi}}&SoruGoster={{$SssKategori.No}}">{{$SssKategori.Ad}}</a>
       </td>
       <td align=center>
        <a href="javascript:OzelPencere('{{$ASSayfa}}SssKategoriDuzenle&SssKategoriNo={{$SssKategori.No}}','Duzenle',500,200,0,1)"><img src="{{$WebAdminResimler}}/duzenle.gif" border=0 alt="Düzenle"></a>&nbsp;
        <a onclick="return confirm('{{$SssKategori.Ad}} kategorisini silmek istediðinize emin misiniz?')" href="{{$Burasi}}&KategoriSil={{$SssKategori.No}}"><img src="{{$WebAdminResimler}}/sil.gif" border=0 alt="Sil"></a>
      </td>
     </tr>
    {{/foreach}}
   </table>
   {{else}}
      <br><br><b><center>Kategori bulunamadý!</center></b><br>
   {{/if}}
   <br>
   <table border=0 align=center width=100% cellpadding=3 cellspacing=0>
   <tr class=tabbas1><td colspan=2>YENÝ SSS KATEGORÝ EKLE</td></tr> 
   <form action="{{$Burasi}}" method="POST" onsubmit="javascript: return kontrol(this);">
    <tr>
     <td class=tdbaslik>Kategori Ad</td>
     <td align=right><input type=text name="N_KategoriAd" alt="Kategori Ad"></td>
    </tr>
    <tr>
     <td class=tdbaslik>Açýklama</td>
     <td align=right><input type=text name="Aciklama" alt="Açýklama"></td>
    </tr>
    <tr>
     <td colspan=2 align=right>
      <input type="submit" name="KategoriEkle" value="Ekle" class="onay">
     </td>
    </tr>
   </form>
   </table>
  </td>
  <td valign=top align=center>
  <table border=0 width=100% cellpadding=0 cellspacing=0>
  {{if $SoruVar}}
   <tr><td>
    <table border=0 align=left width=100% cellpadding=3 cellspacing=0>
    <tr class=tabbas3><td colspan=3>SSS&nbsp;{{$SssKategoriAd}}</td></tr>
    <form action="{{$Burasi}}" method="POST">
     {{foreach item=Soru from=$Sorular name=Sorular}}
     {{if $smarty.foreach.Sorular.iteration is odd}} <tr class=tabloliste1>{{else}} <tr class=tabloliste2>{{/if}} 
      <td width=6%>
        {{if $Soru.Yukari}}
        <a href="{{$Burasi}}&SoruYukari=1&SoruNo={{$Soru.No}}&SoruGoster={{$SoruGoster}}">
         <img border=0 src="{{$WebAdminResimler}}/yukari.gif" alt="Yukarý">
        </a>
        {{/if}}
        {{if $Soru.Asagi}}
        <a href="{{$Burasi}}&SoruAsagi=1&SoruNo={{$Soru.No}}&SoruGoster={{$SoruGoster}}">
          <img border=0 src="{{$WebAdminResimler}}/asagi.gif" alt="Aþagý">
        </a>
        {{/if}}
      </td>
      <td>{{$Soru.Soru}}</td>
      <td align=right>
       <a href="javascript:OzelPencere('{{$ASSayfa}}SssSoruDuzenle&SoruNo={{$Soru.No}}&SoruGoster={{$SoruGoster}}','Duzenle',500,420,0,1)"><img src="{{$WebAdminResimler}}/duzenle.gif" border=0></a>&nbsp;
       <a onclick="return confirm('Soruyu silmek istediðinize emin misiniz?')" href="{{$Burasi}}&Sil={{$Soru.No}}&SoruGoster={{$SoruGoster}}"><img src="{{$WebAdminResimler}}/sil.gif" border=0></a>
      </td>
     </tr>
     {{/foreach}}

    </form>
    </table>
    
    </td></tr>
   {{else}}
     {{if $Listelendi eq 1}} <br><br><b><center>{{$SssKategoriAd}}&nbsp; soru bulunamadý!</center></b><br>{{/if}}
   {{/if}}
   <tr><td>
   {{if $Listelendi eq 1}}
    <table border=0 width=100% cellpadding=3 cellspacing=0>
    <form action="{{$Burasi}}&SoruGoster={{$SoruGoster}}" method="POST" onsubmit="javascript: return kontrol(this);">
     <tr class=tabbas3><td colspan=2>{{$SssKategoriAd}} KATEGORÝSÝNE YENÝ SORU EKLE</td></tr>
     <tr>
       <td><b>Soru:</b><br><textarea name="N_YeniSoru" cols=40 rows=5 alt="Soru"></textarea></td>
       <td align=left><b>Cevap :</b><br><textarea name="N_YeniCevap" cols=40 rows=5 alt="Cevap"></textarea></td>
     </tr>
     <input type=hidden name="YeniSoruKategoriNo" value="{{$SssKategoriNo}}">
     <tr>
      <td colspan=2 align=right>
        <input type="submit" name="YeniSoruEkle" value="Ekle" class="onay">
      </td>
     </tr>
    </form>
    </table>
   {{/if}}
   </td></tr></table>
  </td>
 </tr>
</table>
{{/strip}}
