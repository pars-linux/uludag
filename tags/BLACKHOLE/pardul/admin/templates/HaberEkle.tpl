{{strip}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<script type="text/javascript" src="{{$AdminAnaSayfa}}/jscript/fckeditor.js"></script>
<script type="text/javascript" src="{{$AdminAnaSayfa}}/jscript/jscript.js"></script>
<script language="JavaScript" src="jscript/popcalendar.js"></script>
<script>TamEkran();</script>
<script type="text/javascript">
window.onload = function()
{
	var oFCKeditor = new FCKeditor( 'Icerik','980','450','Default' ) ;
	oFCKeditor.BasePath	= 'jscript/' ;
	oFCKeditor.ReplaceTextarea() ;
}
</script>
  <table border=0 width="50%">
   <form method="POST" action="{{$Burasi}}" onsubmit="return kontrol(this)">
  	<tr><td colspan="3"><textarea cols=65 rows=16 id="Icerik" name="Icerik"  alt="Haber Ýçeriði"></textarea></td></tr>
 	<tr><td>Baþlýk</td><td><input size=30 type="text" name="N_Baslik" alt="Haber Baþlýðý"></td></tr>
 	<tr>
      <td>Haber Tarihi</td>
      <td>
	  	<input type="text" name="Tarih" size="20" value="{{$BugunTarihi}}">&nbsp;
	    <input type="image" src="resimler/ew_calendar.gif" alt="Tarih Seçiniz..." onClick="popUpCalendar(this, this.form.Tarih,'dd.mm.yyyy');return false;"></TD>
   	  </td>
    </tr>
 	<tr><td>Aktif mi?</td><td> <input type="checkbox" name="Durum" {{if $HaberBilgiler.Durum eq 'Aktif'}} checked="true" {{/if}}></td></tr>
 	<tr><td>Resim</td><td><input size=30 type="text" name="Resim"></td></tr>
 	<tr><td colspan="3" align=right><hr><input type="submit" name="Gonder" value="Yeni Ekle"></td></tr>
		<input type="hidden" name="HaberNo" value="{{$HaberNo}}">
   </form>
  </table>
{{include file="Footer.tpl"}}
{{/strip}}