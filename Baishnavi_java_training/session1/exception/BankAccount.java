package session1.exception;

// handles account balance and withdrawal logic
public class BankAccount {

    private double balance;

    // constructor to initialize balance
    public BankAccount(double balance) {
        this.balance = balance;
    }

    // method to withdraw money
    public void withdraw(double amount) throws InsufficientBalanceException {

        // check if sufficient balance is available
        if (amount > balance) {
            throw new InsufficientBalanceException("Not enough balance");
        }

        balance -= amount;
        System.out.println("Withdrawal successful. Remaining balance: " + balance);
    }
}