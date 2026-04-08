package session1.exception;

import java.util.Scanner;

public class BankApp {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        // take initial balance input
        System.out.print("Enter initial balance: ");
        double balance = sc.nextDouble();

        BankAccount account = new BankAccount(balance);

        try {
            // take withdrawal input
            System.out.print("Enter amount to withdraw: ");
            double amount = sc.nextDouble();

            account.withdraw(amount);

        } catch (InsufficientBalanceException e) {
            System.out.println("Error: " + e.getMessage());

        } finally {
            System.out.println("Transaction process completed");
        }

        sc.close();
    }
}