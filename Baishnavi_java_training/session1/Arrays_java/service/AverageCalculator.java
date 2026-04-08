package Baishnavi_java_training.session1.Arrays_java.service;

public class AverageCalculator {

    public double calculateAverage(int[] numbers) {

        if (numbers == null) {
            throw new IllegalArgumentException("Array cannot be null");
        }

        if (numbers.length == 0) {
            System.out.println("Array is empty. Average = 0");
            return 0;
        }

        long sum = 0; // long to prevent overflow

        for (int num : numbers) {
            sum += num;
        }

        return (double) sum / numbers.length;
    }
}