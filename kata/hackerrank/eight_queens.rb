
def EightQueens(strArr)
  strArr.each do |attack_queen|
    ax= attack_queen[1].to_i
    ay= attack_queen[3].to_i

    strArr.each do |defense_queen|
      next if attack_queen == defense_queen

      dx= defense_queen[1].to_i
      dy= defense_queen[3].to_i


      # vertical or horizontal move
      if ax == dx || ay == dy
        return attack_queen
      end

      # diagonal move
      if (ax-dx).abs == (ay-dy).abs
        return attack_queen
      end

    end
  end

  return true
end


test_case = ["(2,1)", "(4,2)", "(6,3)", "(8,4)", "(3,5)", "(1,6)", "(7,7)", "(5,8)"] 
result = EightQueens(test_case)
puts result

test_case2 = ["(2,1)", "(5,3)", "(6,3)", "(8,4)", "(3,4)", "(1,8)", "(7,7)", "(5,8)"]
result = EightQueens(test_case2)
puts result

test_case3 = [ "(2,1)", "(4,3)", "(6,3)", "(8,4)", "(3,4)", "(1,6)", "(7,7)", "(5,8)" ]
result = EightQueens(test_case3)
puts result

=begin
Horizontal or Vertical Move
  x1 == x2 || y1 == y2

Diagonal Move
  abs(x1-x2) == abs(y1-y2)

  2,2
  3,3
  2-3 = 1
  2-3 = 1

  1,1
  3,3
  1-3=2
  3-1=2

1,3   2,3  3,3
1,2   2,2  2,3
1,1   2,1  3,1
=end

