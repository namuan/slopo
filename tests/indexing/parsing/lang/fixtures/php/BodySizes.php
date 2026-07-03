<?php

abstract class Repository
{
    abstract public function abstractMethod(): void;

    public function emptyBody(): void
    {
    }

    #[Deprecated]
    public function annotatedWithLogic(array $items): int
    {
        $total = 0;
        foreach ($items as $item) {
            if ($item > 0) {
                $total += $item;
            }
        }
        return $total;
    }
}
