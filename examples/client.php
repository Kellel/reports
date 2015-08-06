#!/usr/bin/env php
<?php

function usage($argv) {
    echo "Send a job to the report daemon\n";
    echo "Usage: php client.php FILENAME\n";
}

if ($argc != 2) {
    usage($argv);
    return;
};

$filename = $argv[1];

$data = array("filename" => $filename, "user" => "testuser");

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);
$redis->lPush("report-listen-queue", json_encode($data));

?>
