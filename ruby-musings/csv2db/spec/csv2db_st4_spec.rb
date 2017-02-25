#####################################################################################
# (c) carlos@xt6.us 20150328
#####################################################################################

require_relative "../lib/csv2db.rb"

"Describe how the CSV 2 sqlite should work, fifth spec, test_file3.csv"

RSpec.describe "Parsing and loading test_file2.csv and test_file3.csv in the same db file " do

  before(:each) do
    # @m = Csv2Db.new("./tmp/tst4.db" , sep: "|", useheaders: false)
    @m = Csv2Db.new("./tmp/tst4.db")
  end

  it "Also loads a simple, single file, as it did before" do
     @m.loadfile("spec/test_file2.csv", "res", sep: "|", useheaders: false, \
        colspec: ['rir', 'cc', 'type', 'pfx'])
     expect(@m.meta['dbs'][0]['csvfn']).to be == "spec/test_file2.csv"
  end

  it "Correctly loads two files and creates two tables" do
    @m.loadfile("spec/test_file2.csv", "resources", sep: "|", useheaders: false, \
        colspec: ['rir', 'cc', 'type', 'pfx'])
    @m.loadfile("spec/test_file3.csv", "rpkidata", sep: ",", useheaders: false, \
        colspec: ['asn', 'pfx', 'maxlen'])
    #
    metadata = @m.meta
    expect(metadata['dbs'][0]['tblname']).to be == "resources"
    expect(metadata['dbs'][1]['tblname']).to be == "rpkidata"
  end

  it "Allows a join select and produces correct results"

end
