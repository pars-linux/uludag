{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<table width=100% cellspacing=0 cellpadding=0 border=0><tr><td width=200 valign=top>
	<form method=post action="{{$Burasi}}" onsubmit="return kontrol(this)">
	<table width=100% cellpadding=4 cellspacing=0 border=0>
	<tr>
		<td class=tabbas1 colspan=2 align=center>Kay�tl� Sayfalar</td>
	</tr>
	{{foreach item=Sayfa from=$Sayfalar name=Sayfalar}}
	{{if $smarty.foreach.Sayfalar.iteration is odd}}<tr class=tabloliste1> {{else}}<tr class=tabloliste2>{{/if}}
		<td><a href="{{$Burasi}}&Sayfa={{$Sayfa}}">{{$Sayfa}}</a></td>
		<td align=right><a href="{{$Burasi}}&SSayfa={{$Sayfa}}" onclick="return confirm('Sayfa tan�m�n� silmek istedi�inizden emin misiniz');"><img border=0 src="{{$WebAdminResimler}}/sil.gif"></a></td>
	</tr>
	{{/foreach}}
	<tr class=tabbas1>
		<td colspan=2 align=center>Yeni Sayfa:<br>
		    <input type=text name=N_YeniSayfa alt="Yeni Sayfa ad�"></td>
	</tr>
	<tr><td colspan=2 align=right><input type=submit value="Ekle" class=onay></td></tr>
	</table>
	</form>
</td><td valign=top>
	{{if $Uyari}}
		<center>{{include file="HataGoster.tpl" Uyari=$Uyari}}</center><br>
	{{/if}}
	{{if $Bolumler}}
	<table width=100%>
	<tr><td class=tabbas1 colspan=3 align=center><U>D�zenlenen Sayfa:</U> {{$SecilenSayfa}}</td></tr>
	<tr>	
	{{foreach item=Sutun from=$Bolumler}}
		<td width={{$SutunGenislik}}% valign=top><table width=100% border=0 cellpadding=3>
		{{foreach item=Satir from=$Sutun name=Sutun}}
                {{if $smarty.foreach.Sutun.iteration is odd}}<tr class=tabloliste1> {{else}}<tr class=tabloliste2>{{/if}}
			<td width=20 class=tdbaslik>{{$Satir.Satir}}.</td>
			<td align=center>{{$Satir.Isim}}</td>
			<td align=center width=30><a onclick="return confirm('{{$Satir.Isim}} mod�l�n� sayfadan kald�rmak istedi�inize emin misiniz?')" href="{{$Burasi}}&Sayfa={{$SecilenSayfa}}&SBolum={{$Satir.No}}">Sil</a></td>
			<td width=20 align=center>
			<a href="{{$Burasi}}&Sayfa={{$SecilenSayfa}}&YBolum={{$Satir.No}}"><img src="{{$WebAdminResimler}}/yukari.gif" border=0></a>
			<a href="{{$Burasi}}&Sayfa={{$SecilenSayfa}}&ABolum={{$Satir.No}}"><img src="{{$WebAdminResimler}}/asagi.gif" border=0></a>
			</td>
		</tr>
		{{/foreach}}
		</table></td>
	{{/foreach}}
	</tr></table>
	<br>
	<form method=post action="{{$Burasi}}&Sayfa={{$SecilenSayfa}}">
	<table align=center width=100% cellpadding=3 cellspacing=0 border=0>
		<tr>
			<td colspan=2></td><td class=tabbas3>Sayfaya Yeni B�l�m Ekle</td>
		</tr>
		<tr>
			<td align=right colspan=2 width=80%><b>B�l�m Ad� :</b></td>
			<td align=right><select name="YeniBolum" size=10><option value="">Se�iniz -----------------------</option>{{html_options options=$YeniBolumler}}</select></td>
		</tr>
		<tr>
			<td colspan=2 align=right><b>S�tun :</b></td>
			<td align=left><select name="YeniSutun"><option value="">Se�iniz</option>{{html_options options=$YeniSutunlar}}</select></td>
		</tr>
		<tr>
			<td colspan=2 align=right><b>Sat�r :</b></td>
			<td align=left><select name="YeniSatir"><option value="">Se�iniz</option>{{html_options options=$YeniSatirlar}}</select></td>
		</tr>
                <tr>  
                  <td colspan=3 align=right>
                     <input type=checkbox name="TumSayfalardaOlsun" value="Evet" id="Tumunde"><label for="Tumunde">Bu mod�l t�m sayfalara eklensin</label>
                  </td>
                </tr> 
		<tr><td colspan=3 align=right><input type=submit value="Ekle" class=onay></tr>
	</table>
	</form>
		<br>
	<hr>
	
	{{/if}}
</td></tr></table>
{{/strip}}
