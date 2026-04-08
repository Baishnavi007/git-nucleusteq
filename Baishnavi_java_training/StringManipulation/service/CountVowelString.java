package StringManipulation.service;

/*
 * Handles vowel counting
 */
public class CountVowelString {

    public int countVowels(String input) {

        // Edge case: null input
        if (input == null) {
            throw new IllegalArgumentException("Input cannot be null");
        }

        int count = 0;

        // Convert to lowercase for uniformity
        String lower = input.toLowerCase();

        for (int i = 0; i < lower.length(); i++) {
            char ch = lower.charAt(i);

            if (ch == 'a' || ch == 'e' || ch == 'i' ||
                ch == 'o' || ch == 'u') {
                count++;
            }
        }

        return count;
    }
}