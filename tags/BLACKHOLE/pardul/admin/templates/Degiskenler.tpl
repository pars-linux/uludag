{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<table width=100% height=100% border=0>
<tr class=tabbas1><td colspan=2>SÝSTEM DEÐÝÞKENLERÝ</td></tr>
<tr><td width=50% valign=top>
<table cellpadding=0 width=400>
{{foreach item=K from=$Kategoriler}}
	<tr class=tabbas1><td style="cursor: hand;" onclick="BlokSaklaGoster('kategori{{$K.Sira}}');">{{$K.Isim}}</td></tr>
	<tr><td>
		{{if $K.Secili}}
		<div id="kategori{{$K.Sira}}" style="display: block;">
		{{else}}
		<div id="kategori{{$K.Sira}}"style="display: none;">
		{{/if}}
		<table width=100% cellpadding=3 border=0 style="border-collapse:collapse">
		{{foreach item=D from=$K.Degiskenler name=Degiskenler}}
		{{if $smarty.foreach.Degiskenler.iteration is odd}} <tr class=tabloliste1> {{else}} <tr class=tabloliste2> {{/if}}
			<td valign=middle><a href="{{$Burasi}}&No={{$D.No}}">{{$D.Isim}}:</a></td>
			<td>{{$D.Aciklama}}</td>
		</tr>
		{{/foreach}}
		</table>
		</div>
	</td></tr>
{{/foreach}}
</table>
</td><td align=center valign=top>
	{{if $Bilgiler}}
	<form method=post action="{{$Burasi}}&No={{$Bilgiler.No}}">
	<input type=hidden name="Guncelle" value="1">
	<table cellpadding=3 border=0 width=100% align=center>
	<tr>
		<td class=tabbas2 align=right width=50%>{{$Bilgiler.Isim}} :</td>
		<td align=center class=tabbas2>
		{{if $Degerler}}
		<select name="Deger">{{html_options options=$Degerler selected=$Bilgiler.Deger}}</select>
		{{else}}
		<input name="Deger" value="{{$Bilgiler.Deger}}" size=20>
		{{/if}}
		</td>
	</tr>
	<tr><td colspan=2 align=right><input type=submit class=onay value="Kaydet"></td></tr>
	</table>
	</form>
	{{/if}}
	<hr><span class=uyari>Dikkat:</span> Sistem deðiþkenleri iþlem dosyalarýnda (*.php) "$sistem_DegiskenAdi" olarak kullanilir. Ayni degiskeni template dosyasinda { {$sistem_DegiskenAdi} } olarak kullanabilirsiniz.<hr>
</td></tr></table>
{{/strip}}
