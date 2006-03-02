{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<script language=JavaScript src="{{$AdminAnaSayfa}}/jscript/jscript.js"></script>
<script type="text/javascript" src="{{$AdminAnaSayfa}}/jscript/fckeditor.js"></script>
<script language="JavaScript" src="jscript/popcalendar.js"></script>
<script type="text/javascript">
window.onload = function()
{
	var oFCKeditor = new FCKeditor( 'Icerik','100%','450','Default' ) ;
	oFCKeditor.BasePath	= 'jscript/' ;
	oFCKeditor.ReplaceTextarea() ;
}
</script>
<form method="POST" action="{{$Burasi}}" onsubmit="return kontrol(this)" enctype="multipart/form-data">
<table border=0 width="100%">
 <tr>
  <td colspan="2"><textarea name="Icerik" cols=50 rows=10 alt="Özet">{{$Icerik}}</textarea>
    </td>
 </tr>
  <tr>
      <td><br>&nbsp;&nbsp;<b>Son Güncellenme Tarihi</b></td>
      <td>
	  	<br><input type="text" name="Tarih" size="20" value="{{$Tarih}}" disabled>&nbsp;
	   </td>
    </tr>
  <tr><td align="right" colspan="2"><br><hr><input type="submit" name="Guncelle" value="Güncelle"></td></tr>
</table><br>
<input type="hidden" value="{{$No}}" name="No">
</form>
{{/strip}}