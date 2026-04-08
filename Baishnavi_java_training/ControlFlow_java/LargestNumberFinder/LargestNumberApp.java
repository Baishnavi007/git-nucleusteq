
//package Baishnavi_java_training.ControlFlow_java.prime_checker.LargestNumberFinder;

import java.util.Scanner;

public class LargestNumberApp {

    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);
        LargestNumberFinder finder = new LargestNumberFinder();

        System.out.print("Enter first number: ");
        int first = scanner.nextInt();

        System.out.print("Enter second number: ");
        int second = scanner.nextInt();

        System.out.print("Enter third number: ");
        int third = scanner.nextInt();

        int largest = finder.findLargest(first, second, third);

        System.out.println("Largest number is: " + largest);

        scanner.close();
    }
}
