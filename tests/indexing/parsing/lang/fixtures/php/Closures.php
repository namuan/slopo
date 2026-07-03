<?php

class Transformer
{
    public function build(): array
    {
        $doubler = fn(int $x) => $x * 2;

        $this->onComplete = function () {
            echo "done";
        };

        return array_map(fn(int $v) => $v + 1, [1, 2, 3]);
    }
}
