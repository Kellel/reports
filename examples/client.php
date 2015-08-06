<?php

$redis = new Redis();

$data = array("filename" => "testfile.txt", "user" => "testuser");

$redis->connect('127.0.0.1', 6379);
$redis->lPush("report-listen-queue", json_encode($data));

?>
