require 'pry'

puts "
##############################
# tap exercise
##############################
"


# Exercise 1: Implement Object.tap method

(1..10).tap {|x| puts "original: #{x.inspect}"}           # original: 1..10
.to_a.tap {|x| puts "array: #{x.inspect}"}                # array: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
.select {|x| x%2==0}.tap {|x| puts "evens: #{x.inspect}"} # evens: [2, 4, 6, 8, 10]
.map {|x| x*x}.tap {|x| puts "squares: #{x.inspect}"}     # squares: [4, 16, 36, 64, 100]

class Object
  def tap1(&block)
    yield self if block_given? # alt.block.call(self)
    self
  end
end

(1..10).tap1 {|x| puts "original: #{x.inspect}"}           # original: 1..10
.to_a.tap1 {|x| puts "array: #{x.inspect}"}                # array: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
.select {|x| x%2==0}.tap1 {|x| puts "evens: #{x.inspect}"} # evens: [2, 4, 6, 8, 10]
.map {|x| x*x}.tap1 {|x| puts "squares: #{x.inspect}"}     # squares: [4, 16, 36, 64, 100]

# Exercise 2: Improve Object.tap method
# The .tap method only allows you to call public methods of the object. 
# But, sometimes you want to be able to call private methods or access instance variables.

class Object
  def tap2(&block)
    yield self.instance_eval(&block) # self not required
    # self.instance_eval { self }
    self
  end
end

class MyClass
  def initialize
    @var = "instance var"
  end
  def foo
    "MyClass#foo"
  end
end

obj = MyClass.new
puts obj.tap2 { puts @var }.foo  # Outputs: "instance var" and returns: "MyClass#foo"

puts "
##############################
# struct exercise
##############################
"

# Exercise: Implement Struct class from Standard Ruby Library
#
# Task 1: Create a class named ConStruct that replicates the Struct class's behavior. 
# It should create/define a new class with properties and 
# accessors that were passed in to its initializer like so:

class ConStruct
  def initialize(*args, &block)
    args.each do |key, value|
      instance_variable_set :"@#{key}", nil # value

      define_singleton_method key do
        instance_variable_get :"@#{key}"
      end
    end

    if block_given?
      yield self.instance_eval(&block)
    end

  end

  def new(*args)
    instance_variables.each_with_index do |key, idx|
      instance_variable_set :"#{key}", args[idx]
    end

    return self
  end

  def []=(key, value)
    instance_variable_set :"@#{key}", value
  end

  def [](key)
    instance_variable_get :"@#{key}"
  end

end

Product = ConStruct.new(:id, "name")    # Should allow string and symbol names
 
obj = Product.new(123, "Ruby Book")
 
puts obj.name                                # => "Ruby Book"
puts obj["name"] = "Ruby Video Course"       # => "Ruby Video Course"
puts obj[:name]                              # => "Ruby Video Course"

# Clear constant name
Object.send(:remove_const, :Product)

# Task 2: Add option to your ConStruct class that would allow 
# passing a block to initializer and define methods of the class.

Product = ConStruct.new(:id, "name") do
  def to_s
    "<#{self.class} id:#{id} name:'#{name}'>"
  end
end
 
puts Product.new(123, "Ruby Book").to_s      # => <Product id:123 name:'Ruby Book'>


puts "
##############################
# html dsl exercise
##############################
"

# Exercise: Build custom DSL to generate HTML
# There are many DSLs that allow you to generate HTML code. In this exercise, you are asked to build the one similar to the arbe gem's syntax.

# Here is an example of arbe code:
# html = Arbre::Context.new do
# h2 "Why is Arbre awesome?"
# ul do
#  li "The DOM is implemented in ruby"
#  li "You can create object oriented views"
#  li "Templates suck"
# end
# end

# puts html.to_s
# <h2>Why is Arbre awesome?</h2>
# # <ul>
# #   <li>The DOM is implemented in ruby</li>
# #   <li>You can create object oriented views</li>
# #   <li>Templates suck</li>
# # </ul>

# Task 1: Build the following HTML class that supports the DSL.

class HTML
  def initialize(&block)
    if block_given?
      binding.pry



    end
  end
end

html = HTML.new do
  h2 "Why is Arbre awesome?"

  ul do
    li "The DOM is implemented in ruby"
    li "You can create object oriented views"
    li "Templates suck"
  end
end


# Task 2: Allow adding attributes to the tags as it is shown in the example below.

# html = HTML.new do
#  ul id: "nav", class: "list-squares" do
#    li "The DOM is implemented in ruby"
#  end
# end

# Task 3: Add p tag to your DSL code and run it. What happens? Are your paragraph tags rendered? If not, explain why?

# html = HTML.new do
#   h1 "Super buper title"
#   p "Some paragraph."
#   p "Another paragraph."
# end

