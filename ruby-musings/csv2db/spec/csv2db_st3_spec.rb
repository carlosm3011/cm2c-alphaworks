#####################################################################################
# (c) carlos@xt6.us 20150326
#####################################################################################

require_relative "../lib/csv2db.rb"

"Describe how the CSV 2 sqlite should work, third spec, test_file3.csv"

RSpec.describe "Parsing and loading test_file3.csv: " do

  before(:each) do
    @m = Csv2Db.new("./tmp/tst_f2_3.db" , sep: "|", useheaders: false)
  end

  it "Loads correctly and has more than 100 rows" do
    @m.loadfile("spec/test_file2.csv")
    expect(@m.linecnt).to be > 100
  end

  it "Has exactly 7 columns" do
    @m.loadfile("spec/test_file2.csv")
    expect(@m.colcnt).to be == 7
  end

end
