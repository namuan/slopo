<?php

class Outer
{
    public function outerMethod(): void
    {
        echo "outer";
    }

    private function makeInner(): object
    {
        return new class {
            public function innerMethod(): string
            {
                return "inner";
            }
        };
    }
}
