{{strip}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<script type="text/javascript" src="{{$AdminAnaSayfa}}/jscript/fckeditor.js"></script>
<script type="text/javascript" src="{{$AdminAnaSayfa}}/jscript/jscript.js"></script>
<script language="JavaScript" src="jscript/popcalendar.js"></script>
<script>TamEkran();</script>
<script type="text/javascript">
window.onload = function()
{
	var oFCKeditor = new FCKeditor( 'Icerik','100%','450','Default' ) ;
	oFCKeditor.BasePath	= 'jscript/' ;
	oFCKeditor.ReplaceTextarea() ;
	var ooFCKeditor = new FCKeditor( 'HaberSlogan','100%','450','Ek' ) ;
	ooFCKeditor.BasePath	= 'jscript/' ;
	ooFCKeditor.ReplaceTextarea() ;
}
</script>
<title>Haber Düzenleme</title>
<table border="0" width="100%">
<TR>
<TD width="100%">
  <table border=0 width=100%>
   <form method="POST" action="{{$Burasi}}" onsubmit="return kontrol(this)">
	<tr>
	<td colspan="2"><textarea  name="Icerik"  alt="Haber Ýçeriði">{{$Icerik}}</textarea></td>
	<TD width="250"><textarea name="HaberSlogan">{{$HaberSlogan}}</textarea>
	</TD>
	</tr>
  </table>
</TD>
</tr>
<tr>
<TD>
  <table border=0 width="100%">
 	<tr><td>Haber No</td><br><td><input type="text" name="HaberNo" value="{{$HaberNo}}" disabled></td></tr>
 	<tr><td>Baþlýk</td><td><input size=30 type="text" name="N_Baslik" alt="Haber Baþlýðý" value="{{$Baslik}}"></td></tr>
 	<tr>
      <td>Haber Tarihi</td>
      <td>
	  	<input type="text" name="Tarih" size="20" value="{{$Tarih}}">&nbsp;
	    <input type="image" src="resimler/ew_calendar.gif" alt="Tarih Seçiniz..." onClick="popUpCalendar(this, this.form.Tarih,'dd.mm.yyyy');return false;"></TD>
   	  </td>
    </tr>
 	<tr><td>Kaynak</td><td><input size=30 type="text" name="Kaynak" value="{{$Kaynak}}"></td></tr>
	<tr><td>Aktif mi? <input type="checkbox" name="Durum" {{if $Durum eq 'Aktif'}} checked="true" {{/if}}></td></tr>
	<tr><td colspan="2" align=left><hr><input type="submit" name="Guncelle" value="Güncelle"></td></tr>
		<input type="hidden" name="HaberNo" value="{{$HaberNo}}">
   </form>
  </table>
{{include file=Footer.tpl}}
{{/strip}}