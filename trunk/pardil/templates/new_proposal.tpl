#include $site_path + "templates/header.tpl"
<div id="content">
  #if $revision
  <h2>Yeni Sürüm</h2>
  #else
  <h2>Yeni Öneri</h2>
  #end if

  #def printError($s)
    #if $errors.has_key($s)
      #echo """<div class="error_msg">%s</div>""" % ($errors[$s])
    #end if
  #end def

  #def printValue($s, $t='')
    #if not $errors.has_key($s) and $posted_values.has_key($s)
      #echo $posted_values[$s]
    #else
      #echo $t
    #end if
  #end def

  #if $status == 'done_revision'
    <p>$pid numaralı önerinin $version numaralı sürümü eklendi.</p>
    <ul>
      <li><a href="viewproposal.py?pid=$pid&amp;version=$version">Öneriyi Göster</a></li>
    </ul>
  #else if $status == 'done_new'
    <p>$pid numaralı öneri eklendi.</p>
    <ul>
      <li><a href="viewproposal.py?pid=$pid&amp;version=1.0.0">Öneriyi Göster</a></li>
    </ul>
  #else:
  <form action="new_proposal.py" method="post">
    <fieldset>
      <legend>Öneri Bilgileri</legend>
      <div class="required">
        <label for="p_title">Başlık:</label>
        <input type="text" id="p_title" name="p_title" value="#echo $printValue('p_title', '') #" />
        #echo $printError('p_title')
      </div>
      #if $revision
      <input type="hidden" name="pid" value="$pid" />
      <div class="optional">
        <label>Mevcut Sürüm No.:</label>
        <input id="version" name="version" type="text" value="$version" readonly="readonly" />
      </div>
      <div class="required">
        <label for="p_version">Değişiklik Derecesi:</label>
        <select id="p_version" name="p_version">
          <option value="3">Düşük</option>
          <option value="2">Orta</option>
          <option value="1">Yüksek</option>
        </select>
        #echo $printError('p_version')
      </div>
      #end if
    </fieldset>
    <fieldset>
      <legend>Öneri Özeti</legend>
      <div class="required">
        <textarea class="widetext" id="p_summary" name="p_summary">#echo $printValue('p_summary', '') #</textarea>
        #echo $printError('p_summary')
      </div>
    </fieldset>
    <fieldset>
      <legend>Amaç</legend>
      <div class="required">
        <textarea class="widetext" id="p_purpose" name="p_purpose">#echo $printValue('p_purpose', '') #</textarea>
        #echo $printError('p_purpose')
      </div>
    </fieldset>
    <fieldset>
      <legend>Öneri İçeriği</legend>
      <div class="required">
        <textarea class="widetext" id="p_content" name="p_content">#echo $printValue('p_content', '') #</textarea>
        #echo $printError('p_content')
      </div>
    </fieldset>
    <fieldset>
      <legend>Çözüm</legend>
      <div class="required">
        <textarea class="widetext" id="p_solution" name="p_solution">#echo $printValue('p_solution', '') #</textarea>
        #echo $printError('p_solution')
      </div>
    </fieldset>
    #if $revision
    <fieldset>
      <legend>Sürüm Notları</legend>
      <div class="required">
        <textarea class="widetext" id="p_changelog" name="p_changelog">#echo $printValue('p_changelog', '') #</textarea>
        #echo $printError('p_changelog')
      </div>
    </fieldset>
    #end if
    <fieldset>
      <button type="submit" name="new_proposal" value="1">Gönder</button>
    </fieldset>
  </form>
  #end if
</div>
#include $site_path + "templates/footer.tpl"
