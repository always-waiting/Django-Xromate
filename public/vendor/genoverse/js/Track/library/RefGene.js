Genoverse.Track.RefGene = Genoverse.Track.extend({
  labels : true,
  repeatLabels: true,
  bump: true,
  id     : 'refgene',
  name   : 'UCSC: refGene',
  height : 60,
  autoHeight: false,
  hideEmpty : false,
  url    : '/api/annodb/ucscrefgene?chr=__CHR__&start=__START__&end=__END__',
  category: "UCSC refGene",
  info:  "Refgene",
  featureHeight: 6,
  tags: [],
  controls: [],

  parseData: function (data) {
    for (var i = 0; i < data.length; i++) {
      var f = data[i];
      f.id = f.name;
      f.label= f.geneName || f.name;
      f.start= f.txStart;
      f.end= f.txEnd;
      f.strand = f.strand == "-" ? -1 : 1;
      this.insertFeature(f);
    }
  },
  populateMenu: function (feature) {
    var menu = {
      title    : feature.label,
      Location : this.browser.chr + ':' + feature.start + '-' + feature.end,
      Name     : feature.name,
      GeneName : feature.geneName
    };
    return menu;
  },
  setFeatureColor: function (feature) {
    var color = '#3BB9FF';
    feature.color = feature.labelColor = color;
  },

  // Different settings for different zoom level
  10000000: { // This one applies when > 10M base-pairs per screen
    labels : false
  },
});
