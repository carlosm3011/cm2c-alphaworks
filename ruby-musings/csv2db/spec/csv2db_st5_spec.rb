#####################################################################################
# (c) carlos@xt6.us 20150327
#####################################################################################

require_relative "../lib/csv2db.rb"

"Describe how the CSV 2 sqlite should work, third spec, test_file3.csv"

RSpec.describe "Parsing and loading test_file2.csv and adding calculated columns: " do
  
  before(:each) do
    @cspec = ['rir', 'cc', 'type', 'prefix', 'size', 'date', 'status']
    @m = Csv2Db.new("spec/test_file2.csv", "tst4.db" , sep: "|", useheaders: false, colspec: @cspec)
    @m.loadfile()
  end

  it "Should name fields according to colspec" do
    v = @m.query_single("select size from rows where rowid = 20")
    expect(v.length).to be  > 0
  end
    
  it "Loads correctly and has more than 100 rows" do
    expect(@m.linecnt).to be > 100
  end
  
  it "Has 7 columns before adding a new one" do
    expect(@m.colcnt).to be == 7
  end

  it "Add one column succeeds and new table has 8 columns" do
    @m.add_calculated_col("size_equiv") do |x|
      nv=x['col4'].to_i+10
      nv.to_s
    end
    expect(@m.colcnt).to be == 8
  end

  it "Calculated values of the new column should be as expected" do
      @m.add_calculated_col("size_equiv") do |x|
        nv=x['size'].to_i+10
        nv.to_s
      end    
      rs = @m.query_single_record("select rowid, size, size_equiv from rows where rowid > 60 limit 1")
      expect(rs['size_equiv']).to be == String(rs["size"].to_i+10)
  end
  
end 