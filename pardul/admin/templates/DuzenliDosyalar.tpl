{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<table width=100% cellpadding=0 cellspacing=0 border=0>
   <tr class=tabbas1><td colspan=2>DÜZENLÝ ÇALIÞAN DOSYALAR</td></tr>
  <tr>
   <td width=30% valign=top>
   <table width=70% align=left border=0 cellpadding=5>
   {{foreach item=Dosya from=$DuzenliDosyalar name=DuzenliDosyalar}}
	{{if $smarty.foreach.DuzenliDosyalar.iteration is odd}} <tr class=tabloliste1> {{else}} <tr class=tabloliste2> {{/if}}
          <td><a href="{{$Burasi}}&Dosya={{$Dosya.No}}">{{$Dosya.Isim}}</a></td>
        </tr>
   {{/foreach}}
   </table>
<br>
</td><td valign=top>
	{{if $Bilgiler}}
	<table width=100% align=center border=0 cellpadding=5>
	<tr>
	<form method=post action="{{$Burasi}}&Dosya={{$Bilgiler.No}}">
	<input type=hidden name=Guncelle value=1>
		<td width=200 class=tabbas2>Dosya:</td>
		<td>{{$Bilgiler.Dosya}}</td>
	</tr>
	<tr>
		<td class=tabbas2>Açýklama:</td>
		<td>{{$Bilgiler.Aciklama}}</td>
	</tr>
	<tr>
		<td class=tabbas2>Aktif:</td>
		<td><input type=checkbox name="AktifPasif" value="1" {{if $Bilgiler.Aktif}}checked{{/if}}></td>
	</tr>
	<tr>
		<td class=tabbas2>Çalýþma Zamaný:</td>
		<td>
		<table width=100% cellpadding=5>
		<tr>
			<td><input id="HerGun" type=radio name="CalismaZaman" value="HerGun" {{if $Bilgiler.HerGun}}checked{{/if}}>
			Her Gün&nbsp;
			<select name="HerGunSaat" onchange="this.form.HerGun.checked=true;">{{html_options options=$HerGunSaatler selected=$Bilgiler.HerGunSaat}}</select>&nbsp;<b>:</b>&nbsp;
			<select name="HerGunDakika">{{html_options options=$HerGunDakikalar selected=$Bilgiler.HerGunDakika}}</select>
			</td>
		</tr>
		<tr>
			<td><input id="SaatBir" type=radio name="CalismaZaman" value="SaatteBir" {{if $Bilgiler.SaatteBir}}checked{{/if}}>
			<select name="SaatteBir" onchange="this.form.SaatBir.checked=true;">{{html_options options=$SaatZamanAraliklar selected=$Bilgiler.SaatteBirAralik}}</select>
			&nbsp;saatte bir defa</td>
		</tr>
		<tr>
			<td><input id="DakikaBir" type=radio name="CalismaZaman" value="DakikadaBir" {{if $Bilgiler.DakikadaBir}}checked{{/if}}>
			<select name="DakikadaBir" onchange="this.form.DakikaBir.checked=true;">{{html_options options=$DakikaZamanAraliklar selected=$Bilgiler.DakikadaBirAralik}}</select>
			&nbsp;dakikada bir defa</td>
		</tr>
		</table>
		</td>
	</tr>
	<tr><td colspan=2 align=right><input type=submit class=onay value="Güncelle"></td></tr>
	</table>
	</form>
	<table width=100% align=center border=0 cellpadding=3 cellspacing=0>
	<tr class=tabbas3><td colspan="2" align=center>Çalýþma Zamanlarý</td></tr>
	<form method=post action="{{$Burasi}}&Dosya={{$Bilgiler.No}}">
	<tr>
		<td width=50%>
		<table align=center cellpadding=5> 
			<tr><td><input type=radio name="ListeTur" value="Gun" {{if $Bilgiler.ListeTur eq "Gun"}}checked{{/if}}>
			Son&nbsp;<input size=2 class=sayi name="GunSayi" value="{{$Bilgiler.GunSayi}}">
			&nbsp;gün içinde</td></tr>
		<tr><td><input type=radio name="ListeTur" value="Defa" {{if $Bilgiler.ListeTur eq "Defa"}}checked{{/if}}>
			Son&nbsp;<input size=2 class=sayi name="DefaSayi" value="{{$Bilgiler.DefaSayi}}">
			&nbsp;defa çalýþmasý</td></tr>
		</table>
		</td>
		<td align=center><input class=onay type=submit value="Listele"></td>
	</tr>
	</form>
	<tr><td colspan=2>
		<table width=100% cellpadding=3 border=1>
		{{foreach item=Calisma from=$Bilgiler.Calismalar}}
		<tr>
			<th width=20 align=center>-</th>
			<td>{{$Calisma}}</td>
		</tr>
		{{/foreach}}
		</table>
	</td></tr>
	</table>
	<br>
	{{/if}}
</td></tr></table>
{{/strip}}
