Genoverse.Track.OMIMMorbidmap = Genoverse.Track.extend({
  id : "omimSyndrome",
  name: "OMIM Syndromes",
  category: "OMIM Syndromes",
  info: "OMIM Syndromes - Syndromes without phenotype maps",
  tags: [ "syndrome", "omim" ],
  height: 160,
  autoHeight: true,
  hideEmpty: false,
  featureHeight: 4,
  labels: true,
  repeatLabels: true,
  bump: true,
  url: "/api/annodb/omimmorbidmap?chr=__CHR__&start=__START__&end=__END__",

  parseData: function(data) {
    for( var i in data) {
      var f = data[i];
      f.id = f.phenotypeMimNumber;
      f.name = f.phenotype + " (" + f.phenotypeMappingKey + ")";
      f.label = f.id + ": " + f.name;
      this.insertFeature(f);
    }
  },

  setFeatureColor: function(f) {
    switch ( f.phenotypeMappingKey ) {
      case 4: f.color = '#008000';break;
      case 3: f.color = "#008080";break;
      case 2: f.color = "#A0A0A0";break;
      case 1: f.color = "#C0C0C0";break;
      default: f.color = "#F0F0F0";break;
    }
    f.labelColor = f.color;
  },
  populateMenu: function(a,b) {
      var url = '/entry/omim/' + a.mimNumber;
      var c={},
      d = [
        ["title", '<a target="_blank" href="/entry/omim/'+a.id+'">' + a.name +'</b></a>'],
        ["Location", a.chr+ ":" + a.start+ "-" + a.end],
        ["CytoLocation", a.cytoLocation],
        ["Genemap MIM Number", a.geneMapExists ? '<a target="_blank" href="/entry/omim/'+a.mimNumber+'"><b>'+a.mimNumber+'</b></a>' : null],
        ["Gene Symbols", a.geneSymbols],
      ], f;
      for (f in d) "undefined" !== typeof d[f][1] && (c[d[f][0]] = d[f][1]);
      return $.extend(c, b)
    }
});
