{{strip}}
{{if $Duzenlenecek eq "Link"}}
<title>Link D�zenleme</title>
  <table border=1 width=100% cellpadding=2>
   <form action="{{$Burasi}}" method="POST" onsubmit="javascript: return kontrol(this);">
     <tr class=tabbas1><td colspan=2>SORU D�ZENLEME</td></tr>
     <tr>
       <td class=tdbaslik>Link</td>
       <td>
        <input type=text name="N_Link" value="{{$Link}}">
      </td>
     </tr>
      <tr>
       <td class=tdbaslik>Link A��klama</td>
       <td>
        <input type=text name="N_Aciklama" value="{{$Aciklama}}">
      </td>
     </tr>
     <input type=hidden name="LinkKategoriNo" value="{{$LinkKategoriNo}}">
     <input type=hidden name="LinkNo" value="{{$LinkNo}}">
     <tr>
      <td colspan=2 align=right>
        <input type="submit" name="LinkGuncelle" value="G�ncelle" class="onay">
      </td>
     </tr>
   </form>
  </table>
{{/if}}

{{include file="Footer.tpl"}}
{{/strip}}
