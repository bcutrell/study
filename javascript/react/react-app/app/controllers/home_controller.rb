class HomeController < ApplicationController

  def index

    # initial state
    @account = {
      name: 'Fred',
      holdings: [],
      target: nil
    }
 
  end
end
