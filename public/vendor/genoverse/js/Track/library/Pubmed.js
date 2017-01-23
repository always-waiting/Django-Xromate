Genoverse.Track.Pubmed = Genoverse.Track.extend({
  id      : 'pubmed',
  name    : 'Pubmed',
  category: 'Pubmed',
  info    : "Pubmed - CNV diseases related pubmed articles",
  url    : 'http://192.168.4.168:9009/api/genoverse/pubmed?chr=__CHR__&start=__START__&end=__END__',
  height  : 50,
  autoHeight  : true,
  hideEmpty   : false,
  featureHeight: 6,
  tags: [],
  labels: true,
  repeatLabels: true,
  bump: true,

  parseData: function(data) {
    for (var i = 0; i < data.length; i++) {
      var f = data[i];
      f.location = "chr" + f.chr + ':' + f.start + "-" + f.end;
      f.id = f.location;
      f.name = f.location;
      f.label= f.name;
      this.insertFeature(f);
    }
  },
  populateMenu: function (feature) {
    var menu = {
      title    : feature.name,
      Location : "chr" + feature.chr + ':' + feature.start + "-" + feature.end,
      Gainloss : feature.gainloss,
      Cytoband : feature.cytoband,
      Size     : feature.size,
      Description: feature.description,
      Pubmeds  : feature.pmid
    };
    return menu;
  },
  setFeatureColor: function (f) {
    f.featureColor = f.color = f.gainloss == "mosaic" ? "#00FF00" : (f.gainloss == "loss" ? "#FF0000" : "#0000FF");
  },
});
