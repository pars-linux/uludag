{{strip}}
	<br><center class=uyari>{{$AdSoyad}}</center><br>
	<title>�ye Yorum ve G�r��leri</title>
	{{if $GorusSayi}}
		<table border=0 width=100% cellpadding=3>
			<tr class=tabbas1><td>G�R��LER�</td><td align=right>{{$GorusSayi}} G�r��</td></tr>
			{{foreach item=Gorus from=$Gorusler}}
				<tr class=tabbas3><td colspan=2><b>{{$Gorus.Tarih}}</b></td></tr>
				<tr class=tabbas2><td colspan=2>{{$Gorus.Gorus}}</td></tr>
			{{/foreach}}
		</table>	
	{{/if}}
	<br>
    {{if $YorumSayi}}
        <table border=0 width=100% cellpadding=3>
            <tr class=tabbas1><td colspan=3>HABER YORUMLARI</td><td align=right>{{$YorumSayi}} Yorum</td></tr>
            {{foreach item=Yorum from=$Yorumlar}}
                <tr>
				<td>{{$Yorum.Tarih}}</td>
				</tr>
                <tr class=tabbas2>
                <td colspan=3>{{$Yorum.Yorum}}</td>
                 <td><a href="{{$Burasi}}&UyeNo={{$UyeNo}}&YorumNo={{$Yorum.No}}&Onay={{if $Yorum.Durum eq 'Onaylandi'}}Onaylanmadi{{else}}Onaylandi{{/if}}" title="Yorumu Yay�nlamak i�in T�klay�n�z!">{{$Yorum.Durum}}</a></td>
                </tr>
            {{/foreach}}
        </table>
    {{/if}}
	{{if NOT $YorumSayi AND NOT $GorusSayi}}
		<br><br><center class=uyari>�yenin g�r�� veya yorumu bulunmamaktad�r.</center>
	{{/if}}	
{{/strip}}
