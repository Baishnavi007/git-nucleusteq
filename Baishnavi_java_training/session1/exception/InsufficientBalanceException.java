package session1.exception;

// custom exception for insufficient balance
public class InsufficientBalanceException extends Exception {

    public InsufficientBalanceException(String message) {
        super(message);
    }
}