defmodule Closures do
  def build do
    doubler = fn x -> x * 2 end
    Enum.map([1, 2, 3], fn v -> doubler.(v) + 1 end)
  end
end
