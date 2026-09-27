package Baishnavi_java_training.session1.Arrays_java.service;

public class SortService {

    public void bubbleSort(int[] numbers) {

        if (numbers == null) {
            throw new IllegalArgumentException("Array cannot be null");
        }

        if (numbers.length <= 1) {
            return; // already sorted
        }

        int n = numbers.length;

        for (int i = 0; i < n - 1; i++) {
            boolean isSwapped = false;

            for (int j = 0; j < n - i - 1; j++) {

                if (numbers[j] > numbers[j + 1]) {

                    int temp = numbers[j];
                    numbers[j] = numbers[j + 1];
                    numbers[j + 1] = temp;

                    isSwapped = true;
                }
            }

            if (!isSwapped) {
                break; // optimization
            }
        }
    }
}