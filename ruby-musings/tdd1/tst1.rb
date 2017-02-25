"Describe como hacer unas cuentitas"

require_relative "calky"

RSpec.describe Calky do
  m = Calky.new
	it "1 mas 2 tendria que dar 3" do
		expect(m.add(1,2)).to eq(3)
	end

	it "3 mas 4 tendria que dar 7" do
		expect(m.add(3,4)).to eq(7)
	end
  
  it "2 por 3 llueve" do
    expect(m.prod(2,3)).to eq(6)
  end
  
end
