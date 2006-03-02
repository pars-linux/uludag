{{strip}}
{{if $Duzenlenecek eq "Kategori"}}
<title>Kategori Düzenleme</title>
  <table border=1 width=100% cellpadding=3>
   <form action="{{$Burasi}}" method="POST" onsubmit="javascript: return kontrol(this);">
     <tr class=tabbas1><td colspan=2>KATEGORÝ DÜZENLEME</td></tr>
     <tr>
       <td class=tdbaslik>Kategori Ad</td>
       <td><input type="text" name="N_KategoriAd" alt="Kategori Ad" value="{{$KategoriAd}}"></td>
     </tr>
     <tr>
       <td class=tdbaslik>Açýklama</td>
       <td><input size="50" type="text" name="Aciklama" alt="Açýklama" value="{{$Aciklama}}"></td>
     </tr>
     <input type=hidden name="SssKategoriNo" value="{{$SssKategoriNo}}">
     <tr>
      <td colspan=2 align=right>
        <input type="submit" name="KategoriGuncelle" value="Güncelle" class="onay">
      </td>
     </tr>
   </form>
  </table>
{{/if}}

{{include file="Footer.tpl"}}
{{/strip}}
