{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<table border=0 width=100% align=center style="border-collapse:collapse" cellpadding=5>
 <tr class=tabbas1 height=33><td colspan=3>Sayfa Ýstatistikleri</td></tr>
</table>
<br><br>
<table border=0 cellpadding="0" cellspacing="0" width="100%" align="right">
<form name="DosyaDuzenle" method="POST" action="{{$Burasi}}">

	<tr class="tabbas2">
		<td align="center">
		<select name="Kategori">
			<option value="">Kategori Seçiniz...</option>
			<option value="Haberler">Haberler</option>
			<option value="Etkinlikler">Etkinlikler</option>
			<option value="Hukuki_Alt_Yapi">Hukuki Alt Yapý</option>
			<option value="PatentNedir">Barkod Nedir</option>
			
		</select>
		</td>
		<td align="left">
		<INPUT type="submit" name="Listele" value="Listele" class=onay>
		</td>
	</tr>
</form>
</table>
<br>
<br>
<br>
<table border=0 cellpadding="0" cellspacing="0" width="100%">
<form name="EkDuzenle" method="POST" action="{{$Burasi}}">
{{if $Istatistikler}}
	{{if $Yazar}}
	
	{{else}}
<tr>
	<td colspan="4">
		<table border=0 cellpadding="0" cellspacing="0" width="100%">
		<tr>
				<td>
				<FIELDSET style="display:block; position:relative; top:0; width=100%">
				<LEGEND>{{$Kategori}}' nin Genel Ýstatistikler</LEGEND>	
				 <b>Ana Sayfa&nbsp;&nbsp;&nbsp;:&nbsp;</b> <font color="#00aaa0" size="2">{{$Toplam}}</font> <br>
				 <b>Alt Kategori:</b> <font color="#00aaa0" size="2">{{$AltKategoriToplam}}</font> 	
				</fieldset><br><br>
				</td>
				
			</tr>
		</table>
	</td>
</tr>
{{/if}}
<tr class="tabbas1">
	<td>Baþlýk</td>
	<td>Kayýt No</td>
	<td>Hit</td>
	<td>Ek</td>
</tr>
{{foreach item=Istatistikler from=$Istatistikler name=Istatistikler}}
{{if $smarty.foreach.Istatistikler.iteration is odd}}<tr class=tabloliste1>{{else}}<tr class=tabloliste2>{{/if}}
<td align="left"><b>{{$Istatistikler.Konu}}</b></td>
<td align="left">{{$Istatistikler.Sayfa}}</td>
<td align="left">{{$Istatistikler.Hit}}</td>
<td align="left">
<input name="{{$Istatistikler.No}}" type="text" value="{{$Istatistikler.Ek}}" onChange="this.style.backgroundColor='#c4ffa7'" style="text-align:right" size="8" maxlength="5">
</td>
</tr>
{{/foreach}}
<tr><td colspan="4" align="right"><br><br>
<input name="Kategori" type="hidden" value="{{$Kategori}}">
<INPUT type="submit" name="EkDuzenle" value="Düzenle" class="onay">
</td></tr>
{{/if}}
</form>
</table>
{{/strip}}
