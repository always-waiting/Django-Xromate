Genoverse.Track.OMIMGenemap = Genoverse.Track.extend({
  id     : 'omimGeneMap',
  name   : 'OMIM: GeneMap',
  category: "OMIM GeneMaps",
  info : "OMIM - Online Mendelian Inheritance in Man",
  tags: "GeneMap",
  height : 160,
  autoHeight: true,
  hideEmpty : false,
  featureHeight: 6,
  labels: true,
  repeatLabels: true,
  bump: true,
  url: "/api/annodb/omimgenemap/__CHR__:__START__-__END__",

  parseData: function(d) {
    for( var g in d){
      var f = d[g];
      f.id = f.mimNumber;
      f.name = f.approvedGeneSymbol;
      f.start = f.chromosomeLocationStart;
      f.end = f.chromosomeLocationEnd;
      f.label = f.id;
      if ('undefined' !== typeof f.phenotypeMapList && f.phenotypeMapList.length > 0) {
        for (var p in f.phenotypeMapList) {
          var pheno = f.phenotypeMapList[p].phenotypeMap;
          if ('undefined' !== typeof pheno.phenotypeMimNumber && pheno.mimNumber !== pheno.phenotypeMimNumber) {
            if('undefined' === typeof f.phenotypeMimNumber) {
              f.phenotypeMimNumber = pheno.phenotypeMimNumber;
            } else {
              if ($.isArray(f.phenotypeMimNumber)) {
                f.phenotypeMimNumber.push(pheno.phenotypeMimNumber);
              } else {
                f.phenotypeMimNumber = [f.phenotypeMimNumber, pheno.phenotypeMimNumber];
              }
            }
          }
        }
      }
      if('undefined' !== typeof f.phenotypeMimNumber){
        f.label = f.name ? f.name : '';
        this.insertFeature(f);
      }
    }
  },

  setFeatureColor: function(f) {
    switch ( f.confidence ) {
      case 'C': f.color = '#008000';break;
      case 'P': f.color = "#008080";break;
      case 'L': f.color = "#A0A0A0";break;
      case 'I': f.color = "#C0C0C0";break;
      default: f.color = "#F0F0F0";break;
    }
    f.labelColor = f.color;
  },
  populateMenu: function(a,b) {
      var url = '/entry/omim/' + a.mimNumber;
      var c={},
      d = [
        ["title", '<a target="_blank" href="/entry/omim/'+a.mimNumber+'">' + a.name +'</b></a>'],
        ["Location", a.chromosome + ":" + a.chromosomeLocationStart + "-" + a.chromosomeLocationEnd],
        ["CytoLocation", a.cytoLocation],
        ["MIM number", '<a target="_blank" href="/entry/omim/'+a.mimNumber+'"><b>'+a.mimNumber+'</b></a>'],
        ["Phenotype MIM", $.isArray(a.phenotypeMimNumber) ? a.phenotypeMimNumber.map(function(v){
          return '<a target="_blank" href="/entry/omim/'+v+'"><b>'+v+'</b></a>';
        }).join(',') :'<a target="_blank" href="/entry/omim/'+a.phenotypeMimNumber+'"><b>'+a.phenotypeMimNumber+'</b></a>'],
        ["Gene", a.geneName],
        ["Confidence", a.confidence],
        ["GeneSymbols", a.geneSymbols],
        ["Mapping method", a.mappingMethod]
      ], f;
      for (f in d) "undefined" !== typeof d[f][1] && (c[d[f][0]] = d[f][1]);
      return $.extend(c, b)
    }
});
