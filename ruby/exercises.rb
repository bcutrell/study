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

# refactor ->
# Class.new do
# end

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

# use & to convert Proc <-> block


def tmp
  [:h2, :ul, :li].each do |m|
    define_singleton_method m do |text|
      if block_given?
        yield self.instance_eval(&block)
      end

      "<#{m}>#{text}</#{m}>"
    end
  end
  yield self.instance_eval(&block) if block_given?
end

class HTML < BasicObject

  def initialize(&block)
    @rendered_html = ""
    instance_eval(&block)
  end

  def method_missing(tag, *args, &block)
    properties = ""

    if args.first.is_a?(::Object::Hash)
      properties = args.shift.map { |p| p.join("=")} * " " 
    end

    @rendered_html << "<#{tag}> #{properties}"

    if block
      @rendered_html << instance_eval(&block)
    else
      @rendered_html << "#{args.first}"
    end

    @rendered_html << "</#{tag}>"
  end

  def render
    @rendered_html
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
puts html.render


# Task 2: Allow adding attributes to the tags as it is shown in the example below.

html = HTML.new do
  ul id: "nav", class: "list-squares" do
    li "The DOM is implemented in ruby"
  end
end
puts html.render

# Task 3: Add p tag to your DSL code and run it. What happens? Are your paragraph tags rendered? If not, explain why?

html = HTML.new do
  h1 "Super buper title"
  p "Some paragraph."
  p "Another paragraph."
end
puts html.render


puts "
##############################
# rails magic exercise
##############################
"

=begin
Exercise: Implement Rails methods and features
This exercise is an individual work. Please try to solve all the tasks yourself. If you can't, this means that you need to review the course content again. If after reviewing the course, you are still having trouble resolving the tasks below, please contact me. I will try to guide you through and direct you in the right direction.



Task 1: Implement Rails application configuration syntax.

All Rails apps store configuration settings in application.rb and environments/{production|etc}.rb files.

An example code from environments directory may looks something like this:

TestApp::Application.configure do
  # Settings specified here will take precedence over those in config/application.rb
 
  # Code is not reloaded between requests
  config.cache_classes = true
 
  # Full error reports are disabled and caching is turned on
  config.consider_all_requests_local       = false
  config.action_controller.perform_caching = true
 
  # Disable Rails's static asset server (Apache or nginx will already do this)
  config.serve_static_assets = false
  
  # ...
end
# Accessing configuration settings
Rails.application.config


Task 1a: Create TestApp::Application class.

Because implementing the exact syntax is not the core purpose of this exercise, please simplify the syntax above to the one below.

TestApp::Application.configure do
  # Code is not reloaded between requests
  config[:cache_classes] = true
 
  # Full error reports are disabled and caching is turned on
  config[:consider_all_requests_local]       = false
  config[:action_controller]                 = true
  
  # ...
end


Implement TestApp::Application class. It must have .configure method that takes a block. Also, make sure that the code in the provided block has access to config method (or Hash, up to you).

Task 1b: Create TestApp::Application.conf configuration accessor method.

Now that we have our configuration class. Add .conf method that would return our application settings.

TestApp::Application.configure do
  config[:cache_classes]     = true
  config[:action_controller] = true
end
 
# Accessing configuration settings
TestApp::Application.conf[:cache_classes]                # => true
 
TestApp::Application.configure do
  config[:cache_classes]     = false
end
 
TestApp::Application.conf[:cache_classes]                # => false
TestApp::Application.conf[:action_controller]            # => true


Task 2: Implement Rails model association methods.

ActiveRecord  makes it really easy to create classes with associated database tables. Also, it makes creating associations between your models even easier by providing you methods like belongs_to, has_one, etc.

Here is an excerpt from the Rails documentation.

class Project < ActiveRecord::Base
  belongs_to              :portfolio
  has_one                 :project_manager
  has_many                :milestones
  has_and_belongs_to_many :categories
end
The project class now has the following methods (and more) to ease the traversal and manipulation of its relationships:

Project#portfolio, Project#portfolio=(portfolio), Project#portfolio.nil?
Project#project_manager, Project#project_manager=(project_manager), Project#project_manager.nil?,
Project#milestones.empty?, Project#milestones.size, Project#milestones, Project#milestones<<(milestone), Project#milestones.delete(milestone), Project#milestones.destroy(milestone), Project#milestones.find(milestone_id), Project#milestones.build, Project#milestones.create
Project#categories.empty?, Project#categories.size, Project#categories, Project#categories<<(category1), Project#categories.delete(category1), Project#categories.destroy(category1)


Task 2a: Think and try to explain to yourself or your teammate how you would implement those methods.

Task 2b: Go through the documentation and think about different ways you would implement all those features/methods.

Task 3: Think of any Rails magic and try to explain to yourself or your teammate different ways you could implement it.
=end
