{{strip}}
{{if $Duzenlenecek eq "Soru"}}
<title>Soru Düzenleme</title>
  <table border=1 width=100% cellpadding=2>
   <form action="{{$Burasi}}" method="POST" onsubmit="javascript: return kontrol(this);">
     <tr class=tabbas1><td colspan=2>SORU DÜZENLEME</td></tr>
     <tr>
       <td class=tdbaslik>Soru</td>
       <td><textarea name="N_Soru" cols=60 rows=12 alt="Soru">{{$Soru}}</textarea></td>
     </tr>
     <tr>
       <td class=tdbaslik>Cevap</td>
       <td><textarea name="N_Cevap" cols=60 rows=12 alt="Cevap">{{$Cevap}}</textarea></td>
     </tr>
     <input type=hidden name="SoruKategoriNo" value="{{$SoruKategoriNo}}">
     <input type=hidden name="SoruNo" value="{{$SoruNo}}">
     <tr>
      <td colspan=2 align=right>
        <input type="submit" name="SoruGuncelle" value="Güncelle" class="onay">
      </td>
     </tr>
   </form>
  </table>
{{/if}}

{{include file="Footer.tpl"}}
{{/strip}}
