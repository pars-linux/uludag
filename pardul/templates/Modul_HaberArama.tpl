{{strip}}
{{include file="ModulTop.tpl" bgcolor="$sistem_Modul_HaberArama"}}
<TABLE border=0 cellpadding="1" width="100%">
  <TR>
   <TD valign="middle" align="center">
           <TABLE border=0 align="center">
         <TR>
         <FORM method="POST" action="{{$SSayfa}}Haberler">
         <TD><STRONG>{{t}}Haberler içinde Ara{{/t}}</STRONG></TD>
        </TR>
        <TR><TD><INPUT type="text" name="Anahtar" maxlength="30" value="Aranacak Kelimeler..." onfocus="if ( value == 'Aranacak Kelimeler...' ) { value = ''; }" onblur="if ( value == '' ) { value = 'Aranacak Kelimeler...'; }"><BR></TD></TR>
         <TR><TD align="right"><INPUT type="submit" name="HaberAra" class="button" value="  {{t}}Ara{{/t}}  "></TD></TR>
        </FORM>
    </TABLE>
   </TD>
  </TR>
</TABLE>
{{include file="ModulFoot.tpl"}}
{{/strip}}
