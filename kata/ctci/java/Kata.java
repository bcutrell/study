public class Kata {
  // 1.1 Implement an algorithm to determine if a string has all unique characters.
  // What if you cannot use additional data structures?
  public static boolean isUniqueChars(String str) {
    if (str.length() > 128) {
      return false;
    }
    boolean[] char_set = new boolean[128];
		for (int i = 0; i < str.length(); i++) {
			int val = str.charAt(i);
			if (char_set[val]) return false;
			char_set[val] = true;
		}
    return true;
  }

  public static void runIsUnique() {
    System.out.println("1.1 Is Unique");
    String[] words = {"abcde", "hello", "apple", "kite", "padle"};
        for (String word : words) {
            System.out.println(word + ": " + isUniqueChars(word));
        }
  }

  // 1.3 Given two strings, write a method to decide if one is a permutation of the other
  public static boolean isPermutation(String str1, String str2) {
      if (str1.length() != str2.length()) {
          return false;
      }

      int[] char_counts = new int[128];
      char[] str1_array = str1.toCharArray();
      for (char c : str1_array) {
          char_counts[c]++;
      }

      for (int i=0; i < str2.length(); i++) {
          int val = (int) str2.charAt(i);
          if (--char_counts[val] < 0) {
              return false;
          }
      }
      return true;
  }

  public static void runIsPermuation() {
      System.out.println("1.2 Is Permutation");
      String word1 = "aabbcc";
      String word2 = "aabbcc";
      System.out.println(word1 + " " + word2 +  ": " + isPermutation(word1, word2));
  }

  public static void main(String[] args) {
    runIsUnique();
    runIsPermuation();
  }
}

