package Baishnavi_java_training.session1.StringManipulation.service;

/*
 * Handles anagram checking
 */
public class AnagramString {

    public boolean areAnagrams(String str1, String str2) {

        // Edge case: null input
        if (str1 == null || str2 == null) {
            throw new IllegalArgumentException("Input cannot be null");
        }

        // Normalize: remove spaces & convert to lowercase
        str1 = str1.replaceAll("\\s", "").toLowerCase();
        str2 = str2.replaceAll("\\s", "").toLowerCase();

        // Length check
        if (str1.length() != str2.length()) {
            return false;
        }

        int[] freq = new int[26];

        // Count characters
        for (int i = 0; i < str1.length(); i++) {
            freq[str1.charAt(i) - 'a']++;
            freq[str2.charAt(i) - 'a']--;
        }

        // Check all values are zero
        for (int num : freq) {
            if (num != 0) {
                return false;
            }
        }

        return true;
    }
}