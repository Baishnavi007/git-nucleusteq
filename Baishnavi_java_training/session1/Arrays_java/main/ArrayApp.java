package Baishnavi_java_training.session1.Arrays_java.main;

import model.ArrayData;
import service.AverageCalculator;
import service.SortService;
import service.SearchService;

import java.util.Scanner;

public class ArrayApp {

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {

        int[] numbers = inputArray();
        ArrayData arrayData = new ArrayData(numbers);

        AverageCalculator avgCalculator = new AverageCalculator();
        SortService sortService = new SortService();
        SearchService searchService = new SearchService();

        while (true) {

            System.out.println("\n===== MENU =====");
            System.out.println("1. Find Average");
            System.out.println("2. Sort Array");
            System.out.println("3. Search Element");
            System.out.println("4. Exit");

            System.out.print("Enter choice: ");
            int choice = scanner.nextInt();

            switch (choice) {

                case 1:
                    double avg = avgCalculator.calculateAverage(arrayData.getNumbers());
                    System.out.println("Average: " + avg);
                    break;

                case 2:
                    sortService.bubbleSort(arrayData.getNumbers());
                    System.out.print("Sorted Array: ");
                    printArray(arrayData.getNumbers());
                    break;

                case 3:
                    System.out.print("Enter element to search: ");
                    int target = scanner.nextInt();

                    int index = searchService.linearSearch(arrayData.getNumbers(), target);

                    if (index != -1) {
                        System.out.println("Element found at index: " + index);
                    } else {
                        System.out.println("Element not found");
                    }
                    break;

                case 4:
                    System.out.println("Exiting...");
                    return;

                default:
                    System.out.println("Invalid choice! Try again.");
            }
        }
    }

    private static int[] inputArray() {

        System.out.print("Enter size of array: ");
        int size = scanner.nextInt();

        if (size < 0) {
            throw new IllegalArgumentException("Size cannot be negative");
        }

        int[] numbers = new int[size];

        if (size == 0) {
            System.out.println("Empty array created.");
            return numbers;
        }

        System.out.println("Enter elements:");

        for (int i = 0; i < size; i++) {
            numbers[i] = scanner.nextInt();
        }

        return numbers;
    }

    private static void printArray(int[] numbers) {

        if (numbers.length == 0) {
            System.out.println("Array is empty");
            return;
        }

        for (int num : numbers) {
            System.out.print(num + " ");
        }
        System.out.println();
    }
}