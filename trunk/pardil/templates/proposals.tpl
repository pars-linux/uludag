#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Öneriler</h2>
  <table>
    <tr>
      <th>No</th>
      <th>Başlık</th>
    </tr>
    #for $i in $proposals
    <tr>
      <td><a href="viewproposal.py?pid=$i.pid&amp;version=$i.version">$i.pid</a></td>
      <td><a href="viewproposal.py?pid=$i.pid&amp;version=$i.version">$i.title</a></td>
    </tr>
    #end for
  </table>
</div>
#include $site_path + "templates/footer.tpl"
