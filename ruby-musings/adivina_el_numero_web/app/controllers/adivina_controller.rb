class AdivinaController < ApplicationController
  def index
    if params[:guess] == "0" then
      @fase = 1
      @secreto = rand(10)
    else
      @fase = 2
      @secreto = params[:secreto]
    end
  end
end
