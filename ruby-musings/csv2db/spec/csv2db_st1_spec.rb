#####################################################################################
# (c) carlos@xt6.us 20150323
#####################################################################################

require_relative "../lib/csv2db.rb"

"Describe how the CSV 2 sqlite should work, first spec"

RSpec.describe "Parsing and loading test_file1.csv" do

  before(:each) do
    @m = Csv2Db.new("./tmp/tst_f1.db")
    @m.loadfile("spec/test_file1.csv", useheaders: true)
  end

  it "Should create an object instance and the constructor should accept to args" do
    expect(@m).not_to eq(nil)
  end

it "Should have csv file metadata 1" do
    #puts @m.meta['dbs'][0]["csvfn"]
    csvmeta = @m.getmeta("spec/test_file1.csv")
    expect(@m.meta["dbs"][0]["csvfn"]).to eq("spec/test_file1.csv")
  end

  it "Should have csv file metadata 2" do
    expect(@m.dbs[0]['csvfn']).to eq("spec/test_file1.csv")
    expect(@m.dbs[0]['dbfn']).to eq("./tmp/tst_f1.db")
    expect(@m.dbs[0]['linecnt']).to eq(5)
    expect(@m.dbs[0]['colcnt']).to eq(3)
  end

  it "Should open test_file1.csv and return 5 rows and 3 columns in the metadata" do
    expect(@m.linecnt).to eq(5)
    expect(@m.colcnt).to eq(3)
  end

  it "In file test_file1.csv, each row should have 3 fields" do
    @m.csvdata.each do |row|
      expect(row.length).to eq(3)
    end
  end

  it "SQL query should run on test_file1.csv and not return nil" do
    expect(@m.query("select * from rows")).not_to eq(nil)
  end

  it "In file test_file1.csv, row 3 has 2nd column == 1.70" do
    q = @m.query("select * from rows")
    expect(q[2][1]).to eq("1.70")
  end

end
