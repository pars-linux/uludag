{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<script type="text/javascript" src="{{$AdminAnaSayfa}}/jscript/fckeditor.js"></script>
<script type="text/javascript" src="{{$AdminAnaSayfa}}/jscript/jscript.js"></script>

<script>
function SayfaGonder(No)
        {
        document.ListeForm.SayfaNo.value = No;
        document.ListeForm.submit();
        }

</script>
<table width=30% cellpadding=4 cellspacing=0 border=0 align="left">
	<tr>
		<td class=tabbas1 colspan=2 align=center>Kayýtlý Menu Yapýsý</td>
	</tr>
	{{section name=i loop=$Sayfalar}}
	<tr class=tabloliste1>
		<td ><br><br><a href="{{$Burasi}}&Sayfa={{$Sayfalar[i].Adres}}"><b>{{$Sayfalar[i].Baslik}}</b></a>
		{{if $Sayfalar[i].Yukari}}
       		 &nbsp;<a href="{{$Burasi}}&KYukari=1&No={{$Sayfalar[i].No}}"><img border=0 src="{{$WebAdminResimler}}/yukari.gif" alt="Yukarý">&nbsp;</a>
        {{/if}}
        {{if $Sayfalar[i].Asagi}}
       		&nbsp;<a href="{{$Burasi}}&KAsagi=1&No={{$Sayfalar[i].No}}"><img border=0 src="{{$WebAdminResimler}}/asagi.gif" alt="Aþagý"></a>
        {{/if}}
		</td>
		<td align=right><a href="{{$Burasi}}&SSayfa={{$Sayfalar[i].No}}" onclick="return confirm('Sayfa tanýmýný silmek istediðinizden emin misiniz');"><img border=0 src="{{$WebAdminResimler}}/sil.gif"></a></td>
	</tr>
       {{section name=j loop=$Sayfalar[i].AltMenu}}
	    <tr>
			<td >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#8355;&#187;&nbsp;<a href="{{$Burasi}}&Sayfa={{$Sayfalar[i].AltMenu[j].Adres}}">{{$Sayfalar[i].AltMenu[j].Baslik}}</a> 
				{{if $Sayfalar[i].AltMenu[j].Yukari}}
       		 		&nbsp;<a href="{{$Burasi}}&AYukari=1&No={{$Sayfalar[i].AltMenu[j].No}}"><img border=0 src="{{$WebAdminResimler}}/yukari.gif" alt="Yukarý">&nbsp;</a>
       			{{/if}}
       			{{if $Sayfalar[i].AltMenu[j].Asagi}}
       					&nbsp;<a href="{{$Burasi}}&AAsagi=1&No={{$Sayfalar[i].AltMenu[j].No}}"><img border=0 src="{{$WebAdminResimler}}/asagi.gif" alt="Aþagý"></a>
        		{{/if}}
			</td>
	      	<td align=right><a href="{{$Burasi}}&SSayfa={{$Sayfalar[i].AltMenu[j].No}}" onclick="return confirm('Sayfa tanýmýný silmek istediðinizden emin misiniz');"><img border=0 src="{{$WebAdminResimler}}/sil.gif"></a></td>
	      </tr>
	   {{/section}}
	 {{/section}}	
	<tr class=tabbas1>
		<td colspan=2 align=center><a href="{{$ASSayfa}}SSMModulEkle" class="menu">Yeni Sayfa Ekle</a><br>
	</tr>
	
</table>

{{/strip}}
