<?php

class TaskRunner
{
    public function makeTask(string $label): callable
    {
        $run = function () use ($label) {
            echo $label;
        };
        return $run;
    }
}
