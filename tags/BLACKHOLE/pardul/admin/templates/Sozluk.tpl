{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<script language="JavaScript" src="jscript/popcalendar.js"></script>
<br>
<table border=0 cellpadding="5" width="100%">
<TR>
<td>
<FIELDSET style="display:block; position:relative; top:0; width=100%">
<LEGEND>Terimsel S�zc�k Ekle</LEGEND>
<table border=0 cellpadding="0" cellspacing="0" width="80%">
	<form name="HaberDuzenle" method="POST" action="{{$Burasi}}">
	 <tr>
     <td><br>&nbsp;&nbsp;S�zc�k</td>
	  <TD colspan="2"><br><INPUT type="text" name="Sozcuk" size="25" maxlength="255">
	  </TD>
    </tr>
    <tr>
      <tr>
      <TD><br>&nbsp;&nbsp;A��klama</TD>
	  <td><textarea  name="Aciklama"  alt="S�zc���n Anlam�" cols=50 rows=10></textarea></td>	 
	  </tr>
    <tr>
       <td align="right" colspan="4"><br><hr><INPUT type="submit" name="Ekle" value="Ekle" accesskey="D"></td>
    </tr>
	</form>
</table>
<br>
Not: Eklemi� oldu�unuz haberin i�eri�ini, haber g�ncelle sayfas�ndan olu�turabilirsiniz.
</fieldset>
</td>
<TD valign="top" align="center">
<FIELDSET style="width=100%">
<LEGEND>Terimsel S�zc�k Ara</LEGEND>
  <table border=0 width="100%">
   <form method="POST" action="{{$Burasi}}" onsubmit="return kontrol(this)">
	<tr><td>Aranacak Kelime</td><td><input size=30 type="text" name="Anahtar" alt="Anahtar Kelime"></td></tr>
    <tr><td colspan="3" align=right><hr><input type="submit" name="YaziAra" value="G�nder"></td></tr>
		<input type="hidden" name="No" value="{{$No}}">
   </form>
  </table>
  
</FIELDSET>
</TD>
</TR>
<TR><TD colspan="2">
<br>
<table border=0 cellpadding="5" width="100%">
<TR>
<TD valign="top">
	<FIELDSET>
	<LEGEND>Terimsel S�zc�kler</LEGEND>
	<table border=0 width="100%">
	 <tr>
	  <td><b>Kelime</b></td>
	  <td><b>A��klama</b></td>
	  <td><b>D�zenle</b></td>
	  <td><b>Sil</b></td>
	 </tr>
	 <tr><td colspan="6"><hr noshade="true" size="1"></td></tr>
	{{foreach item=TumSozcukler from=$TumSozcukler name=TumSozcukler}}
	 <tr>
	      <input type="hidden" name="No" value="{{$TumSozcukler.No}}">
	  <td><b>{{$TumSozcukler.Kelime}}</b></td>
	  <td>{{$TumSozcukler.Aciklama}}</td>
	  <td><a href="javascript:OzelPencere('{{$ASSayfa}}SozlukDuzenle&No={{$TumSozcukler.No}}','Oku',500,400,1,1);" title="Kelimeyi D�zenlemek i�in T�klay�n�z."><img src="{{$WebAdminResimler}}/duzenle.gif" border=0 alt="D�zenle"></a></td>
	  <TD><a href="{{$Burasi}}&KelimeSil=true&SilNo={{$TumSozcukler.No}}"><img src="{{$WebAdminResimler}}/sil.gif" border="0" alt="kelimeyi Silmek i�in T�klay�n�z!" onClick="return confirm('Kelimeyi Silmek istedi�inizden emin misiniz?')"></a></TD>
	  </tr>
	  <tr><td colspan="4"><hr></td></tr>
	{{/foreach}}
	</table>
	</FIELDSET>
</TD>
</TR>
</table>

</td></TR></table>
{{/strip}}