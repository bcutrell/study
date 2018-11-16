public class Kata {
  // Implement an algorithm to determine if a string has all unique characters. 
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

  // Given two strings, write a method to decide if one is a permutation of the other

  public static void main(String[] args) {
    runIsUnique();
  }
}

