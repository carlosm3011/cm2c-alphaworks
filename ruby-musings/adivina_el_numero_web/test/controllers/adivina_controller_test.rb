require 'test_helper'

class AdivinaControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get adivina_index_url
    assert_response :success
  end

end
