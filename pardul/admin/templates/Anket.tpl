{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<script language=JavaScript src="{{$AdminAnaSayfa}}/jscript/picker.js"></script>
<br>
<table border=0 cellpadding="5" width="100%">
<TR>
<TD valign="top">
	<FIELDSET>
	<LEGEND>Anketler D�zenleme</LEGEND>
	<table border=0 width="100%">
	 <tr>
	  <td><b>Anket Ad</b></td>
	  <td><b>Anket T�r</b></td>
	  <td><b>Grafik T�r</b></td>
	  <td><b>Aktif/Pasif</b></td>
	  <td><b>�yelik Durum</b></td>
	  <td><b>D�zenle</b></td>
	  <td><b>Sil</b></td>
	 </tr>
	 <tr><td colspan="6"><hr noshade="true" size="1"></td></tr>
	{{foreach item=TumAnketler from=$TumAnketler name=TumAnketler}}
	 <tr>
	      <input type="hidden" name="AnketNo" value="{{$TumAnketler.AnketNo}}">
	  <td><b>{{$TumAnketler.AnketAd}}</b></td>
	  <td>{{$TumAnketler.AnketTur}}</td>
	  <td>{{$TumAnketler.GrafikTur}}</td>
	  <td><a href="{{$Burasi}}&AnketNo={{$TumAnketler.AnketNo}}&Aktif={{if $TumAnketler.AnketAktif eq 'Aktif'}}Pasif{{else}}Aktif{{/if}}" title="Anketi Aktif veya Pasif Yapmak i�in T�klay�n�z!">{{$TumAnketler.AnketAktif}}</a></td>
	  <td><a href="{{$Burasi}}&AnketNo={{$TumAnketler.AnketNo}}&Uyelik={{if $TumAnketler.AnketUyelik eq 'Zorunlu'}}Zorunlu De�il{{else}}Zorunlu{{/if}}" title="Anketi �yelikli Yapmak i�in T�klay�n�z!">{{$TumAnketler.AnketUyelik}}</a></td>
	  <td><a href="{{$Burasi}}&AnketNo={{$TumAnketler.AnketNo}}" title="Anketi D�zenlemek i�in T�klay�n�z."><img src="{{$WebAdminResimler}}/duzenle.gif" border=0 alt="D�zenle"></a></td>
	  <TD><a href="{{$Burasi}}&AnketSil=true&SilAnketNo={{$TumAnketler.AnketNo}}"><img src="{{$WebAdminResimler}}/sil.gif" border="0" alt="Anketi Silmek i�in T�klay�n�z!" onClick="return confirm('Anketi Silmek istedi�inizden emin misiniz?')"></a></TD>
	 </tr>
	{{/foreach}}
	</table>
	</FIELDSET>
	<a href="javascript:OzelPencere('{{$ASSayfa}}Sihirbaz_YeniAnket','Sihirbaz',420,300,1,1)">Yeni Anket</a>
</TD>
{{if $Sorular}}
<TD valign="top">
	<FIELDSET><LEGEND>Anket Detaylar�</LEGEND>
	<form name="AnketDuzenle" action="" method="POST">
	 <table border="0" width="100%" cellspacing="3" cellpadding="2" style="border-collapse : separate;">
	 <TR><TD colspan="4">
	 	<input type="hidden" name="SoruNo" value="{{$SoruNo}}">
		<input type="hidden" name="AnketNo" value="{{$AnketNo}}">
	<!--	<input type="hidden" name="SecenekSayi" value="{{$SecenekSayi}}">-->
	 	<input type="text" name="Soru" size="50" value="{{$Soru}}"></TD></TR>
	 {{foreach item=Sorular from=$Sorular name=Sorular}}
	  <TR>
	  	<TD><INPUT type="{{if $AnketTur eq 'Tekli'}}radio{{else}}checkbox{{/if}}" name="sec"></TD>
		<TD><input type="text" size="30" value="{{$Sorular.Secenek}}" name="S{{$Sorular.SecenekNo}}"></TD>
		<TD width="10"><input type="text" name="R{{$Sorular.SecenekNo}}" size="3" style="font-size:1px; background-color:{{$Sorular.Renk}}; width:16px; height:16px" readonly="true" value="{{$Sorular.Renk}}">
		</TD>
		<TD><a href="javascript:TCP.popup(document.forms['AnketDuzenle'].elements['R{{$Sorular.SecenekNo}}']);"><img src="{{$WebAdminResimler}}/colorize.png" border="0" alt="Renk Se�mek i�in Renk Paletini Kullan�n�z!"></a></TD>
		<TD><a href="{{$Burasi}}&AnketNo={{$SeciliAnketNo}}&Sil={{$Sorular.SecenekNo}}"><img src="{{$WebAdminResimler}}/sil.gif" border="0" alt="Se�ene�i Silmek i�in T�klay�n�z!" onClick="return confirm('Se�ene�i Silmek istedi�inizden emin misiniz?')"></a></TD>
	  </TR>
	 {{/foreach}}
	  <TR>
	    <TD>Yeni</TD>
		<TD><input type="text" size="30" name="YeniSecenek"></TD>
		<TD><input type="text" name="YeniRenk" size="3" style="font-size:1px; width:16px; height:16px" readonly="true"></TD>
		<TD><a href="javascript:TCP.popup(document.forms['AnketDuzenle'].elements['YeniRenk']);"><img src="{{$WebAdminResimler}}/colorize.png" border="0" alt="Renk Se�mek i�in Renk Paletini Kullan�n�z!"></a></TD>
	  </TR>
	  <TR><TD colspan="4" align="right">
	  	<input type="submit" name="Submit" value="D�zenle">
	  </TD></TR>
	 </table>
	 </form>
	</FIELDSET>
</TD>
{{/if}}
</TR>
</table>
<br>
{{/strip}}
