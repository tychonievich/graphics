<!DOCTYPE html>
<html lang="en">
<head>
	<title>List of files for "<?=basename(getcwd())?>"</title>
	<meta charset="UTF-8">
	<style>
		table { margin: 1em auto; border-collapse: collapse; border-top: solid black; border-bottom: solid black; }
		thead { border-bottom: thin solid black; }
		tbody tr:nth-child(2n+1) { background: rgba(0,0,0,0.0625); }
		tbody tr td:first-child { font-family: monospace; font-size: 1.25rem; }
		td,th { padding: 0.5ex 1ex; }
		p { max-width: 40em; display: table; margin:auto; }
	</style>
</head>
</body>
<table><thead><tr><th>File name</th><th>Size</th></tr></thead>
<tbody>
<?php
function human_filesize($bytes, $decimals = 2) {
  $sz = 'BKMGTP';
  $factor = floor((strlen($bytes) - 1) / 3);
  $num = $bytes / pow(1024, $factor);
  if ($num < 10) return sprintf("%.{$decimals}f", $num) . @$sz[$factor];
  $decimals -= 1;
  if ($num < 100) return sprintf("%.{$decimals}f", $num) . @$sz[$factor];
  $decimals -= 1;
  if ($num < 1000) return sprintf("%.{$decimals}f", $num) . @$sz[$factor];
  $decimals -= 1;
  return sprintf("%.{$decimals}f", $num) . @$sz[$factor];
}
foreach(glob("*") as $id=>$fn) {
	if (is_dir($fn) || $fn[0] == '.' || $fn == "index.php") continue;
	echo "<tr><td><a href='$fn'>$fn<a></td><td>";
	echo human_filesize(filesize($fn));
	echo "</td></tr>\n";
}
?>
</tbody></table>
<p>
Browsers have different default displays for different file types.
You can use the right-click menu to download files to your computer and open them in a text editor.
You can also use the "view source" option (often Ctrl+U) once you view a page to see the underlying code.
</p>
</body>
</html>
