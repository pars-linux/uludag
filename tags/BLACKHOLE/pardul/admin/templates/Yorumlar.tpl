{{strip}}
<title>Onay Bekleyen Yorumlar</title>
{{if NOT $UyeYorumSayi}}
	<br><center class=uyari>Onay bekleyen yorum bulunmamaktadýr.</center>
{{else}}
<table width=100%><tr><td align=right>Toplam <b>{{$UyeYorumSayi}}</b> Yorum</td></tr></table>
<br>
{{foreach item=Yorum from=$Yorumlar}}
	<table border=1 width=100% cellpadding=5>
	<tr class=tabbas3>
		<td colspan="3">{{$Yorum.UrunAd}}</td>
	</tr>
	<tr class=tabbas2>
		<td>{{$Yorum.AdSoyad}}</td>
		<td align=center width=20%>{{$Yorum.Gorus}}</td>
		<td align=right width=20%>{{$Yorum.Tarih}}</td>
	</tr>
	<tr class=tabbas2>
		<td colspan=3>{{$Yorum.Yorum}}</td>
	</tr>
	<tr>
		<td colspan=3 align=right>
			<a href="{{$Burasi}}&Onayla={{$Yorum.No}}">Onayla</a> &nbsp; | &nbsp;
			<a href="{{$Burasi}}&Sil={{$Yorum.No}}" onclick="return confirm('Üye yorumunu silmek istediðinize emin misiniz?')">Sil</a>
		</td>
	</tr>
	</table>
	<br>
{{/foreach}}
{{/if}}
{{/strip}}
