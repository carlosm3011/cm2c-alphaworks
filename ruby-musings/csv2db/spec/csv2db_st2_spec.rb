#####################################################################################
# (c) carlos@xt6.us 20150326
#####################################################################################

require_relative "../lib/csv2db.rb"

"Describe how the CSV 2 sqlite should work, second spec, test_file2.csv"

RSpec.describe "Parsing and loading test_file2.csv: " do

  before(:each) do
    @m = Csv2Db.new("./tmp/tst_f2_1.db" , useheaders: false)
    @m.loadfile("spec/test_file2.csv")

    @p = Csv2Db.new("./tmp/tst_f2_2.db" , useheaders: false, colspec: ['rir', 'cc', 'restype', 'prefix', 'count'] )
    @p.loadfile("spec/test_file2.csv")
  end

  it "Has more than 100 rows" do
    expect(@m.linecnt).to be > 100
  end

  it "Has more than 3 columns" do
    expect(@m.colcnt).to be > 3
  end

  it "Supports skipping rows"

  it "Runs query with SUM() and colX column names" do
    qr = @m.query("select sum(col4) from rows where col2='ipv4' and col1='BR'")
    tot = qr[0][0]
    expect(tot).to be > 2048
  end

  it "Runs sum() query with query_single and returns a single value" do
    tot = @m.query_single("select sum(col4) from rows where col2='ipv4' and col1='BR'")
    expect(tot).to be > 2048
  end

  it "Runs sum() with friendly column names" do
    tot = @p.query_single("select sum(count) from rows where restype='ipv4' and cc='BR'")
    expect(tot).to be > 2048
  end

end
