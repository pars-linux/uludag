{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<table border=0 width=100% cellpadding=5 cellspacing=0>
 <tr><td colspan=2 class=tabbas1>�PUCU D�ZENLEME</td></tr>
 <tr><td valign=top>
 <table border=0 width=100% cellpadding=5 cellspacing=0>
 <form action="{{$Burasi}}" method="POST" onsubmit="return kontrol(this);">
 <tr>
  <td><b>Yeni �pucu :</b></td></tr>
 <tr>
  <td><textarea name="N_Ipucu" cols=40 rows=5 alt="�pucu">{{$DuzenleMesaj}}</textarea></td>
 </tr>
 <tr>
  <td colspan=2 align=right>
    {{if $DuzenleNo}}
       <input type=hidden name="DuzenleNo" value="{{$DuzenleNo}}">  
       <input type="submit" name="Guncelle" value="G�ncelle" class=onay>
    {{else}}
       <input type="submit" name="Ekle" value="Ekle" class=onay>
    {{/if}}
  </td>
 </tr>
 </form>
</table>
</td>
<td>
{{if $Notlar}}
 <table border=0 width=100% align=center cellpadding=5>
  <tr class=tabbas3><td colspan=2><b>KAYITLI �PU�LARI</b></td></tr>
  {{foreach item=Not from=$Notlar name=Notlar}}
    {{if $smarty.foreach.Notlar.iteration is odd}} <tr class=tabloliste1> {{else}} <tr class=tabloliste2> {{/if}}
     <td>{{$Not.Mesaj}}</td>
     <td>
       <a href="{{$Burasi}}&Duzenle={{$Not.No}}"><img src="{{$WebAdminResimler}}/duzenle.gif" border=0 alt="D�zenle"></a>&nbsp;&nbsp;
       <a onclick="return confirm('Silmek istedi�inize emin misiniz?')" href="{{$Burasi}}&Sil={{$Not.No}}"><img src="{{$WebAdminResimler}}/sil.gif" border=0 alt="Sil"></a>
     </td>
    </tr>
  {{/foreach}}
 </table>
</td></tr>
</table>
{{/if}}


{{/strip}}
