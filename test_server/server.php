<?php

	setcookie("d", "XXX");

	if ($_SERVER['REQUEST_METHOD'] === 'POST') {
		header("HTTP/1.1 500 Internal Server Error");
	}

	//print($_SERVER['HTTP_REFERER']);
	print($_COOKIE["d"])

?>
