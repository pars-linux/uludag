<?php

  function query_proposal_exists($int_id) {
    $str_sql = sprintf('SELECT Count(*) FROM pardil_revisions WHERE proposal=%d', $int_id);
    return (database_query_scalar($str_sql) > 0);
  }
  function query_revision_exists($int_id, $dbl_rev) {
    $str_sql = sprintf('SELECT Count(*) FROM pardil_revisions WHERE proposal=%d AND version=%f', $int_id, $dbl_rev);
    return (database_query_scalar($str_sql) == 1);
  }

?>
