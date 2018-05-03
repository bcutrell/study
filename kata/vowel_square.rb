# https://coderbyte.com/editor/guest:Vowel%20Square:Ruby

=begin
### Challenge

Using the Ruby language, have the function VowelSquare(strArr) take the strArr parameter 
being passed which will be a 2D matrix of some arbitrary size filled with letters from the alphabet, 
and determine if a 2x2 square composed entirely of vowels exists in the matrix. 
For example: strArr is ["abcd", "eikr", "oufj"] then this matrix looks like the following: 

a b c d
e i k r
o u f j 

Within this matrix there is a 2x2 square of vowels starting in the second row 
and first column, namely, ei, ou. If a 2x2 square of vowels is found your program 
should return the top-left position (row-column) of the square, so for this example your program 
should return 1-0. If no 2x2 square of vowels exists, then return the string not found. 
If there are multiple squares of vowels, return the one that is at the most top-left position 
in the whole matrix. The input matrix will at least be of size 2x2. 
=end


VOWELS = ["a", "e", "i", "o", "u"]

require 'pry'
def vowel_square(input)
  nrow = 0

  input.each do |row|
    row = row.split("")

    input.each do |next_row|
      next if row == next_row

      row.each do |col|
        if VOWELS.include? col
          start = row.index(col)
          if [row[start+1], next_row[start], next_row[start+1]].all? { |l| VOWELS.include?(l) }
            puts "todo"
          end
        end

      end

    end

    square = false
    if square
      return nrow, ncol
    end

    nrow += 1
  end

  "not found"
end

input = ["aqrst", "ukaei", "ffooo"]
result = vowel_square(input)
puts result
output = "1-2"


input = ["gg","ff"]
result = vowel_square(input)
puts result
output = "not found"
