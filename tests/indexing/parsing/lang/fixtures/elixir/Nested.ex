defmodule Outer do
  def outer_fun(x) do
    x * 2
  end

  defmodule Inner do
    def inner_fun(y) do
      y + 1
    end
  end
end
