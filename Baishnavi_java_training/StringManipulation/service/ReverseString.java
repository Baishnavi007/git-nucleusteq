package StringManipulation.service;

/*
 * Handles string reversal
 */
public class ReverseString {

    public String reverse(String input) {

        // Edge case: null input
        if (input == null) {
            throw new IllegalArgumentException("Input cannot be null");
        }

        // Edge case: empty string
        if (input.isEmpty()) {
            return input;
        }

        StringBuilder reversed = new StringBuilder();

        // Reverse logic
        for (int i = input.length() - 1; i >= 0; i--) {
            reversed.append(input.charAt(i));
        }

        return reversed.toString();
    }
}