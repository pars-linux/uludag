{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<br>
<table border=0 width="100%">
<tr>
	<td>
<FIELDSET style="display:block; position:relative; top:0; width=100%">
<LEGEND>Ýstatistik Ara</LEGEND>
<table border=0 cellpadding="0" cellspacing="0" width="100%" align="right">
	<form name="IstatistikAra" method="POST" action="{{$Burasi}}">
	 <tr>
     <td><br>&nbsp;&nbsp;<b>Kelime</b></td>
	  <TD colspan="2"><br><INPUT type="text" name="Kelime" size="25" maxlength="255">
	  </TD>
    </tr>
      <tr>
     <td><br>&nbsp;&nbsp;<b>Aranan Sayfa</b></td>
	  <TD colspan="2"><br><INPUT type="text" name="ArananSayfa" size="25" maxlength="255">
	  </TD>
    </tr>
     <tr>
     <td><br>&nbsp;&nbsp;<b>Arama Sayýsý</b></td>
	  <TD colspan="2"><br><INPUT type="text" name="AramaSayisi" size="25" maxlength="255">
	  </TD>
    </tr>
    <tr>
       <td align="right" colspan="4"><br><hr><INPUT type="submit" name="Ara" value="Ara" accesskey="D"></td>
    </tr>
	</form>
</table>
</fielset>
	</td>
</tr>
<tr>
	<td><br><br>
<FIELDSET style="display:block; position:relative; top:0; width=100%">
<LEGEND>Aranan Kelime Ýstatistikleri</LEGEND>
<table border=0 width="100%">
	 <tr class=tabbas1>
	  <td align="left"><b>Kelime</b></td>
	  <td align="left"><b>Aranýlan Sayfa</b></td>
	  <td align="center"><b>Arama Sayýsý</b></td>
	  <td align="center"><b>Bulunan Kayýt Sayýsý</b></td>
	 </tr>
	 <tr><td colspan="6"><hr noshade="true" size="1"></td></tr>
	{{foreach item=ArananKelimeler from=$ArananKelimeler name=ArananKelimeler}}
	 {{if $smarty.foreach.ArananKelimeler.iteration is odd}}<tr class=tabloliste1>{{else}}<tr class=tabloliste2>{{/if}}
	  <td align="left"><b>{{$ArananKelimeler.Kelime}}</b></td>
	  <td align="left">{{$ArananKelimeler.ArananSayfa}}</td>
	  <td align="center">{{$ArananKelimeler.AramaSayisi}}</td>
	  <td align="center">{{$ArananKelimeler.KayitSayisi}}<br><br></td>
	 </tr>
	{{/foreach}}
	</table>
</fieldset>
	</td>
</tr>
</table>
{{/strip}}
