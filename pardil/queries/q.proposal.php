<?php
  function query_proposal_revisionid($int_id, $dbl_revision) {
    $str_sql = sprintf('SELECT id FROM pardil_revisions WHERE proposal=%d and version=%f', $int_id, $dbl_revision);
    return database_query_scalar($str_sql);
  }
?>
