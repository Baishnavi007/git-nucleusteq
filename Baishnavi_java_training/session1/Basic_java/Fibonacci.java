package Baishnavi_java_training.session1.Basic_java;

import java.util.Scanner;

public class Fibonacci {

    // Function to print Fibonacci series up to n terms
    static void printFibonacci(int n) {

        int firstTerm = 0, secondTerm = 1;

        // Loop to print n terms
        for (int i = 1; i <= n; ++i) {

            // Print current term
            System.out.print(firstTerm + " ");

            // Calculate next term
            int nextTerm = firstTerm + secondTerm;

            // Update values for next iteration
            firstTerm = secondTerm;
            secondTerm = nextTerm;
        }
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        // Taking input from user
        System.out.println("Enter number of terms: ");
        int n = sc.nextInt();

        // Printing message
        System.out.println("Fibonacci Series till " + n + " terms:");

        // Function call
        printFibonacci(n);

        sc.close();
    }
}