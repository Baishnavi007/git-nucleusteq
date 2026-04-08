package model;

public class ArrayData {
    private int[] numbers;

    public ArrayData(int[] numbers) {
        if (numbers == null) {
            throw new IllegalArgumentException("Array cannot be null");
        }
        this.numbers = numbers;
    }

    public int[] getNumbers() {
        return numbers;
    }
}
