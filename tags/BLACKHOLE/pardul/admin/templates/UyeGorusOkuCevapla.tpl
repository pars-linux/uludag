{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
{{if $Dizi}}
<table border=0 width=100% cellpadding=3 style="border-collapse:collapse">
<tr class="tabbas1">
  <td>Mesaj</td>
  </tr>
{{foreach item=Dizi from=$Dizi name=Dizi}}
 {{if $smarty.foreach.Dizi.iteration is odd}}<tr class="tabloliste1">{{else}}<tr class="tabloliste2">{{/if}}
  <td>{{$Dizi.Mesaj}}</td>
</tr>

{{/foreach}}
</table>

<br><br>
<table border=0 width=100% style="border-collapse:collapse" cellpadding=3 align=center>
<tr class=tabbas1><td colspan=4 height=33>CEVAP</td></tr>
<form method="POST" action="{{$Burasi}}" name="ListeForm">
<input type=hidden name=SayfaNo value=1>
<input type=hidden name=Ara value=1>
<input type="hidden" value="{{$Dizi.No}}" name="No">
 <tr class=tabloliste1>
   <td>
	
	<textarea name="Mesaj" rows="10" cols="55"></textarea>
   </td>
 </tr>
 <tr><td colspan=4 align=right><input type="submit" name="Cevapla" value="Cevapla" class=onay>
 </td></tr>
</form>
  
 </table>
{{else}}
	<br><br><center class=uyari>Cevabýnýz Baþarý ile Gönderildi!!!</center>
{{/if}}
