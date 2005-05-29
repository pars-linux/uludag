{{strip}}
{{include file="TableTop.tpl"  bgcolor="#FFFFFF"}}
<script language="Javascript">
function SayfaGonder(No)
        {
        document.ListeForm.SayfaNo.value = No;
        document.ListeForm.submit();
        }
</script>
<!-- Kategoriler ve sorular baþladý -->
<table width=100% cellpadding=5 border=0  style="border-collapse:collapse">
<input type=hidden name=SayfaNo value="1">
 {{foreach item=Kategori from=$Kategoriler}}
  <tr><td><h3>{{$Kategori.Ad}}</h3></td></tr>
  {{foreach item=Link from=$Linkler}}
   {{if $Link.KatNo==$Kategori.No}}
      <tr><td><li><a href="{{$Link.Link}}" target="_blank">{{$Link.Aciklama}}</a></td></tr>
   {{/if}}
  {{/foreach}}
  <tr><td><a class="yesil" href="{{$SSayfa}}Linkler">Diðerleri için týklayýnýz.</a></td></tr>
 {{/foreach}}
</table>
{{include file="TableFoot.tpl"}}
{{/strip}}