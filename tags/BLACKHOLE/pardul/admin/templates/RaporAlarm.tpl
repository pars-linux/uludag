{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<table border=0 cellpadding=3 cellspacing=0 width=100%>
<form method=post action="{{$Burasi}}">
<tr class=tabbas1>
	<td colspan=4>KULLANICI ALARM KAYITLARI</td>
</tr>
<tr class=tabloliste1>
	<td colspan=2><input {{if $Bilgiler.Gore eq "UruneGore"}}checked{{/if}} type=radio name="Gore" value="UruneGore" id="UruneGore">�r�n kategorisi </td>
	<td align=left><select name=KategoriNo onchange="this.form.UruneGore.checked=true;"><option value="0">T�m Kategoriler</option>{{html_options options=$Kategoriler selected=$Bilgiler.KategoriNo}}</select></td>
</tr>
<tr>
	<td colspan=2><input {{if $Bilgiler.Gore eq "KullaniciyaGore"}}checked{{/if}} type=radio name="Gore" value="KullaniciyaGore" id="KullaniciyaGore">Kullan�c� E-Posta </td>
	<td align=left><input name=KullaniciAd value="{{$Bilgiler.KullaniciAd}}" onkeypress="this.form.KullaniciyaGore.checked=true;"></td>
</tr>
<tr class=tabloliste1>
	<td colspan=3><input {{if $Bilgiler.Gore eq "EnUzunGore"}}checked{{/if}} type=radio name="Gore" value="EnUzunGore" id="EnUzunGore">En uzun s�re bekleyen</td>
</tr>
<tr>
	<td colspan=2 align=right>Alarm T�r�</td>
	<td align=left>
		<select name=AlarmTur>
		<option value="">T�m�</option>
		{{html_options options=$AlarmTurler selected=$Bilgiler.AlarmTur}}
		</select>
	</td>
</tr>
<tr class=tabloliste1>
	<td colspan=2 align=right>Alarm Durumu</td>
	<td align=left>
		<select name=AlarmDurum>
		<option value="">T�m�</option>
		{{html_options options=$AlarmDurumlar selected=$Bilgiler.AlarmDurum}}
		</select>
	</td>
	<td width=50%>
	<input class=sayi size=3 name="EnUzunSayi" value="{{$Bilgiler.EnUzunSayi}}"> kayd�&nbsp;
	<input class=onay type=submit value="Listele"></td>
</form>
</table>
{{if $Liste}}
<br>
<table cellpadding=5 border=0 width=100%>
	<tr class=tabbas3 >
		<td>Kullan�c�</td>
		<td>�r�n</td>
		<td>Alarm T�r�</td>
		<td>Alarm Durumu</td>
		<td>Alarm Eklenme Tarihi</td>
	</tr>
	{{foreach item=K from=$Liste name=K}}
	{{if $smarty.foreach.K.iteration is odd}} <tr class=tabloliste1> {{else}} <tr class=tabloliste2> {{/if}}
		<td><nobr>{{$K.Kullanici}}&nbsp;({{$K.EPosta}})</nobr></td>
		<td>{{$K.Urun}}</td>
		<td align=center>{{$K.AlarmTur}}</td>
		<td align=center>{{$K.AlarmDurum}}</td>
		<td align=center>{{$K.EklenmeTarih}}</td>
	</tr>
	{{/foreach}}
</table>
{{elseif $SonucYok AND $smarty.post}}
	<br><center class=uyari>Belirtti�iniz �artlar� sa�layan alarm kayd� bulunamad�.</center><br>
{{/if}}
{{/strip}}
