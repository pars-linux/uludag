{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<table border=0 width=100% cellspacing=0 cellpadding=0>
    <tr class=tabbas1><td colspan=4>FAYDALI L�NK KATEGOR�LER�</td></tr>
 <tr>
  <td width=30% valign=top>
   {{if $KategoriVar}}
   <table border=0 width=100% cellpadding=4 cellspacing=0>
    {{foreach item=LinkKategori from=$LinkKategoriler name=LinkKategoriler}}
    {{if $smarty.foreach.LinkKategoriler.iteration is odd}} <tr class=tabloliste1>{{else}} <tr class=tabloliste2>{{/if}}
       <td width=10%>
        {{if $LinkKategori.Yukari}}
        <a href="{{$Burasi}}&Yukari=1&No={{$LinkKategori.No}}"><img border=0 src="{{$WebAdminResimler}}/yukari.gif" alt="Yukar�">&nbsp;</a>
        {{/if}}
        {{if $LinkKategori.Asagi}}
        <a href="{{$Burasi}}&Asagi=1&No={{$LinkKategori.No}}"><img border=0 src="{{$WebAdminResimler}}/asagi.gif" alt="A�ag�"></a>
        {{/if}}
       </td>
       <td>
       <a href="{{$Burasi}}&LinkGoster={{$LinkKategori.No}}">{{$LinkKategori.Ad}}</a>
       </td>
       <td align=center>
        <a href="javascript:OzelPencere('{{$ASSayfa}}LinkKategoriDuzenle&LinkKategoriNo={{$LinkKategori.No}}','Duzenle',500,200,0,1)"><img src="{{$WebAdminResimler}}/duzenle.gif" border=0 alt="D�zenle"></a>&nbsp;
        <a onclick="return confirm('{{$LinkKategori.Ad}} kategorisini silmek istedi�inize emin misiniz?')" href="{{$Burasi}}&KategoriSil={{$LinkKategori.No}}"><img src="{{$WebAdminResimler}}/sil.gif" border=0 alt="Sil"></a>
      </td>
     </tr>
    {{/foreach}}
   </table>
   {{else}}
      <br><br><b><center>Kategori bulunamad�!</center></b><br>
   {{/if}}
   <br>
   <table border=0 align=center width=100% cellpadding=3 cellspacing=0>
   <tr class=tabbas1><td colspan=2>YEN� KATEGOR� EKLE</td></tr> 
   <form action="{{$Burasi}}" method="POST" onsubmit="javascript: return kontrol(this);">
    <tr>
     <td class=tdbaslik>Kategori Ad</td>
     <td align=right><input type=text name="N_KategoriAd" alt="Kategori Ad"></td>
    </tr>
    <tr>
     <td class=tdbaslik>A��klama</td>
     <td align=right><input type=text name="Aciklama" alt="A��klama"></td>
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
  {{if $LinkVar}}
   <tr><td>
    <table border=0 align=left width=100% cellpadding=3 cellspacing=0>
    <tr class=tabbas3><td colspan=3>&nbsp;{{$LinkKategoriAd}}</td></tr>
    <form action="{{$Burasi}}" method="POST">
     {{foreach item=Link from=$Linkler name=Linkler}}
     {{if $smarty.foreach.Linkler.iteration is odd}} <tr class=tabloliste1>{{else}} <tr class=tabloliste2>{{/if}} 
      <td width=6%>
        {{if $Link.Yukari}}
        <a href="{{$Burasi}}&LinkYukari=1&LinkNo={{$Link.No}}&LinkGoster={{$LinkGoster}}">
         <img border=0 src="{{$WebAdminResimler}}/yukari.gif" alt="Yukar�">
        </a>
        {{/if}}
        {{if $Link.Asagi}}
        <a href="{{$Burasi}}&LinkAsagi=1&LinkNo={{$Link.No}}&LinkGoster={{$LinkGoster}}">
          <img border=0 src="{{$WebAdminResimler}}/asagi.gif" alt="A�ag�">
        </a>
        {{/if}}
      </td>
      <td>{{$Link.Aciklama}}</td>
      <td align=right>
       <a href="javascript:OzelPencere('{{$ASSayfa}}LinkDuzenle&LinkNo={{$Link.No}}&LinkGoster={{$LinkGoster}}','Duzenle',500,420,0,1)"><img src="{{$WebAdminResimler}}/duzenle.gif" border=0></a>&nbsp;
       <a onclick="return confirm('Linki silmek istedi�inize emin misiniz?')" href="{{$Burasi}}&Sil={{$Link.No}}&LinkGoster={{$LinkGoster}}"><img src="{{$WebAdminResimler}}/sil.gif" border=0></a>
      </td>
     </tr>
     {{/foreach}}

    </form>
    </table>
    
    </td></tr>
   {{else}}
     {{if $Listelendi eq 1}} <br><br><b><center>{{$LinkKategoriAd}}&nbsp; link bulunamad�!</center></b><br>{{/if}}
   {{/if}}
   <tr><td>
   {{if $Listelendi eq 1}}
    <table border=0 width=100% cellpadding=3 cellspacing=0>
    <form action="{{$Burasi}}&LinkGoster={{$LinkGoster}}" method="POST" onsubmit="javascript: return kontrol(this);">
     <tr class=tabbas3><td colspan=2>{{$LinkKategoriAd}} KATEGOR�S�NE YEN� L�NK EKLE</td></tr>
     <tr>
       <td><b>Link:</b><br>
       <input type=text name="N_YeniLink" value="http://" size="30">
      </td>
      <td><b>Link A��klama:</b><br>
       <input type=text name="N_YeniLinkAciklama"  size="30">
      </td>
     </tr>
     <input type=hidden name="YeniLinkKategoriNo" value="{{$LinkKategoriNo}}">
     <tr>
      <td colspan=2 align=right>
        <input type="submit" name="YeniLinkEkle" value="Ekle" class="onay">
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
