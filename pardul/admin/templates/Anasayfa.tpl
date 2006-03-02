{{strip}}
{{include file="Header.tpl"}}
   <table border=0 width=100% cellpadding=5>		   
	 <tr class=tabbas1><td colspan=2 align=center>ZÝYARETÇÝ SAYISI</td></tr>
	 <tr class=tabloliste1><td><b>Üye Sayýsý</b></td><td align=center><b>{{$UyeGirisSayi}}</b></td></tr>
	 <tr><td><b>Misafir Sayýsý</b></td><td align=center><b>{{$AnonimGirisSayi}}</b></td></tr>
	 <tr class=tabloliste1><td><b>TOPLAM</b></td><td align=center><b><font color=red>{{$ToplamZiyaretci}}</font></b></td></tr>
   </table>	
   <br>
   <table border=0 width=100% cellpadding=5>		   
	 <tr class=tabbas1><td colspan=2 align=center>GENEL</td></tr>
	 <tr class=tabloliste1><td><b><a href="javascript:OzelPencere('{{$ASSayfa}}Yorumlar','Yorumlar',500,600,1,1)">Üye Yorumlarý</a></b></td><td align=center><b>{{$UyeYorumSayi}}</b></td></tr>
	 <tr class=tabloliste1><td><b><a href="{{$ASSayfa}}UyeGorus">Üye Görüþ ve Önerileri</a></b></td><td align=center><b>{{$GorusSayi}}</b></td></tr>
   </table>	
	<br><br>
   <table border=0 cellpadding=0 cellspacing=0 style="border-collapse:collapse;" width=100%>
     <tr><td align=center><a href="{{$ASSayfa}}YonetimMenu">Yönetim Menü Düzenleme</a></td></tr>
	 <tr><td>&nbsp;</td></tr>
     <tr><td align=center><a href="{{$ASSayfa}}YonetimDegiskenler">Sistem Deðiþkenleri</a></td></tr>
   </table>
</td>
<td valign=top>
{{if $Uyarilar}}
  <table align=center border=0 cellspacing=0 cellpadding=2 width=100% style="border-collapse:collapse;">
  <tr class=tabbas1 height=33>
        <td>Uyarý</td>
        <td>Son Gerçekleþme Zamaný</td>
        <td>Gerçekleþme Sayýsý</td>
        <td>Ýþlem</td> 
  </tr>
  {{foreach item=Uyari from=$Uyarilar name=Uyarilar}}
  {{if $smarty.foreach.Uyarilar.iteration is odd}} <tr class=tabloliste1>{{else}}<tr class=tabloliste2>{{/if}}
        <td>{{$Uyari.Mesaj}}</td>
        <td align=center>{{$Uyari.TarihSaat}}</td>
        <td align=center>{{$Uyari.GerceklesmeSayi}}</td>
        <td align=center>
         <a href="{{$Burasi}}&SilUyariNo={{$Uyari.No}}" onclick="return confirm('Uyarý mesajýný silmek istediðinize emin misiniz?');"><img src="{{$WebAdminResimler}}/sil.gif" border=0 alt="Uyarýyý Sil"></a>
        </td>
  </tr>
  {{/foreach}}
  </table>
 {{/if}}
</td>
</tr>
</table>
<!-- Header da acilan tablo kapatiliyor...-->
</td>
</tr>
</table>
{{/strip}}
