defmodule Tasks do
  def make_task(label) do
    fn ->
      IO.puts(label)
    end
  end

  def double_all(numbers) do
    Enum.map(numbers, fn n -> n * 2 end)
  end
end
