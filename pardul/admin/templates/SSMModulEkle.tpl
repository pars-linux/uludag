{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<script type="text/javascript" src="{{$AdminAnaSayfa}}/jscript/fckeditor.js"></script>
<script type="text/javascript" src="{{$AdminAnaSayfa}}/jscript/jscript.js"></script>
<script type="text/javascript">
window.onload = function()
{
	var oFCKeditor = new FCKeditor( 'N_Icerik','850','450','Default' ) ;
	oFCKeditor.BasePath	= 'jscript/' ;
	oFCKeditor.ReplaceTextarea() ;
}
</script>
<script>
function SayfaGonder(No)
        {
        document.ListeForm.SayfaNo.value = No;
        document.ListeForm.submit();
        }

</script>

<table border=0 width=100% cellpadding=5>
	<tr class=tabbas1>
		<td height=33 colspan=4>STANDART SAYFA EKLE</td>
	</tr>
</table>
 <form name="UyeKayit" action="{{$Burasi}}" method=post>
<table border=0 width=100% cellpadding=5>
		<tr>
			<td>
				<b>Menüde Yeralsýn Mý?</b>
			</td>
			 <td>
				<input type="radio" name="N_MenuDurum" value="EvetKategori" onclick="document.getElementById('KategoriId').disabled='true';document.getElementById('KategoriId').selectedIndex=0;"> Evet,YeniBaþlýk Olarak<br><br>
				<input type="radio" name="N_MenuDurum" value="EvetAltKategori" onclick="document.getElementById('KategoriId').disabled='';">Evet, Alt Baþlýk Olarak<br><br>
				<input type="radio" name="N_MenuDurum" value="HayirLink" onclick="document.getElementById('KategoriId').disabled='true';document.getElementById('KategoriId').selectedIndex=0;">Hayýr, Baþka Sayfadan Linki Kendim Veresem
			</td>
		</tr>	
		<tr  bgcolor="#f4f4f4">
				<td>
					<b>Kategori Seçiniz</b>
				</td>
				<td>
				<select name="Kategori" size=10 disabled="true" id="KategoriId">
				<option value="">Seçiniz -----------------------</option>
				{{html_options options=$YeniBolumler}}
				</select>
				</td>
		</tr>
		<tr>
				<td>
					<b>Baþlýk</b>
				</td>
				<td>
					<input type="text" name="N_Baslik" size="25">
				</td>
		</tr>
		<tr bgcolor="#f4f4f4">
				<td>
					<b>Adres</b>
				</td>
				<td>
					<input type="text" name="N_Adres" size="25">
				</td>
		</tr>
	    <tr>
	  	  <TD colspan="2"><textarea name="N_Icerik"alt="Özet"></textarea><br><br><br></TD>
	    </tr>
	    <tr  bgcolor="#f4f4f4">
	    	<td colspan="2" align="right">
	    		<input type="submit" name="MenuEkle" value="E K L E" class="onay"><br><br>
	    </tr>
</TABLE>
</form>
{{/strip}}
