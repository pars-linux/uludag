{{strip}}
{{if $Duzenlenecek eq "Link"}}
<title>Link Düzenleme</title>
  <table border=1 width=100% cellpadding=2>
   <form action="{{$Burasi}}" method="POST" onsubmit="javascript: return kontrol(this);">
     <tr class=tabbas1><td colspan=2>SORU DÜZENLEME</td></tr>
     <tr>
       <td class=tdbaslik>Link</td>
       <td>
        <input type=text name="N_Link" value="{{$Link}}">
      </td>
     </tr>
      <tr>
       <td class=tdbaslik>Link Açýklama</td>
       <td>
        <input type=text name="N_Aciklama" value="{{$Aciklama}}">
      </td>
     </tr>
     <input type=hidden name="LinkKategoriNo" value="{{$LinkKategoriNo}}">
     <input type=hidden name="LinkNo" value="{{$LinkNo}}">
     <tr>
      <td colspan=2 align=right>
        <input type="submit" name="LinkGuncelle" value="Güncelle" class="onay">
      </td>
     </tr>
   </form>
  </table>
{{/if}}

{{include file="Footer.tpl"}}
{{/strip}}
