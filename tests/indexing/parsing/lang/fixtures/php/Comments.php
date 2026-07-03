<?php

class Documented
{
    /**
     * Adds two numbers together.
     */
    public function withComments(int $a, int $b): int
    {
        // line comment
        $sum = $a + $b; # hash comment
        /* block comment */
        $url = "http://not-a-comment";
        return $sum;
    }
}
