package service;

public class SearchService {

    public int linearSearch(int[] numbers, int target) {

        if (numbers == null) {
            throw new IllegalArgumentException("Array cannot be null");
        }

        if (numbers.length == 0) {
            return -1;
        }

        for (int i = 0; i < numbers.length; i++) {
            if (numbers[i] == target) {
                return i;
            }
        }

        return -1;
    }
}