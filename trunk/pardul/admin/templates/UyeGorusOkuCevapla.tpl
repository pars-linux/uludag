<script>TamEkran();</script>
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<script type="text/javascript" src="{{$AdminAnaSayfa}}/jscript/fckeditor.js"></script>

{{if $Dizi}}
<script type="text/javascript">
window.onload = function()
{
	var oFCKeditor = new FCKeditor( 'Mesaj','980','450','Default' ) ;
	oFCKeditor.BasePath	= 'jscript/' ;
	oFCKeditor.ReplaceTextarea() ;
}
</script>
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
	
	<textarea name="Mesaj" rows="5" cols="25"></textarea>
   </td>
 </tr>
 <tr><td colspan=4 align=right><input type="submit" name="Cevapla" value="Cevapla" class=onay>
 </td></tr>
</form>
  
 </table>
{{else}}
	<br><br><center class=uyari>Cevabýnýz Baþarý ile Gönderildi!!!</center>
{{/if}}
